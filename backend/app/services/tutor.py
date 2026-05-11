"""
Socratic tutor service.

Assembles a three-part context package on every call:
  1. Current task  — what the user is doing right now (page, problem, code, ...)
  2. Learner profile — accuracy per topic, known weak areas (from progress.json)
  3. RAG chunks    — relevant course material retrieved from Chroma

Then streams a Gemini response token-by-token via an async generator.
The synchronous Gemini SDK call runs in a thread pool so it never blocks
the FastAPI event loop.
"""

import asyncio
import json
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import AsyncIterator

from google import genai
from google.genai import types

from app.config import settings
from app.services.rag import retrieve_chunks

_client   = genai.Client(api_key=settings.google_api_key)
_executor = ThreadPoolExecutor(max_workers=4)

PROGRESS_FILE: Path = settings.data_dir / "progress.json"


# ---------------------------------------------------------------------------
# Progress helpers
# ---------------------------------------------------------------------------

def _load_progress() -> dict:
    if PROGRESS_FILE.exists():
        return json.loads(PROGRESS_FILE.read_text(encoding="utf-8-sig"))
    return {
        "topics": {},
        "completed_courses": [],
        "completed_problems": [],
        "completed_mcqs": [],
    }


# ---------------------------------------------------------------------------
# Prompt assembly
# ---------------------------------------------------------------------------

def _task_section(ctx: dict) -> str:
    lines = [f"CURRENT TASK: User is on the '{ctx.get('page', 'general')}' page."]
    if ctx.get("course_title"):
        lines.append(f"  Course : {ctx['course_title']}")
    if ctx.get("current_topic"):
        lines.append(f"  Topic  : {ctx['current_topic']}")
    if ctx.get("problem_title"):
        lines.append(f"  Problem: {ctx['problem_title']}")
    if ctx.get("problem_description"):
        lines.append(f"  Description: {ctx['problem_description']}")
    if ctx.get("user_code"):
        lines.append(f"  User's current code:\n```python\n{ctx['user_code']}\n```")
    if ctx.get("failed_tests"):
        lines.append(f"  Failed tests: {json.dumps(ctx['failed_tests'])}")
    if ctx.get("mcq_question"):
        lines.append(f"  MCQ the user is on: {ctx['mcq_question']}")
    return "\n".join(lines)


def _profile_section(progress: dict) -> str:
    topics = progress.get("topics", {})
    weak   = [t for t, s in topics.items() if s.get("accuracy", 1.0) < 0.6]
    strong = [t for t, s in topics.items() if s.get("accuracy", 0.0) >= 0.8]
    lines  = [
        "LEARNER PROFILE:",
        f"  Courses completed : {len(progress.get('completed_courses', []))}",
        f"  Problems solved   : {len(progress.get('completed_problems', []))}",
        f"  Weak topics (<60%): {', '.join(weak) if weak else 'none yet'}",
        f"  Strong topics     : {', '.join(strong) if strong else 'none yet'}",
    ]
    return "\n".join(lines)


def _build_system_prompt(
    socratic_mode: bool,
    ctx: dict,
    progress: dict,
    rag_chunks: list[str],
) -> str:
    if socratic_mode:
        mode_block = (
            "MODE: SOCRATIC\n"
            "Rules:\n"
            "- NEVER give the answer directly.\n"
            "- Respond with exactly ONE targeted question per message.\n"
            "- The question must move the learner one step closer to the answer.\n"
            "- Use the learner profile: focus questions on known weak topics first.\n"
            "- If the learner rephrases the same question 3+ times, give a small partial hint, then ask a follow-up question."
        )
    else:
        mode_block = (
            "MODE: DIRECT\n"
            "Answer clearly and concisely. Personalise using the learner profile and current task — "
            "reference their code or the specific problem where relevant."
        )

    knowledge = "\n\n---\n\n".join(rag_chunks) if rag_chunks else "(No course material retrieved for this query.)"

    return "\n\n".join([
        mode_block,
        _task_section(ctx),
        _profile_section(progress),
        f"RELEVANT COURSE MATERIAL (RAG):\n{knowledge}",
    ])


# ---------------------------------------------------------------------------
# Async streaming entry point
# ---------------------------------------------------------------------------

async def stream_tutor_response(
    message: str,
    socratic_mode: bool,
    ctx: dict,
) -> AsyncIterator[str]:
    """Yield response tokens one at a time as an async generator."""
    progress   = _load_progress()
    rag_chunks = await retrieve_chunks(message, ctx.get("course_id"))
    system     = _build_system_prompt(socratic_mode, ctx, progress, rag_chunks)

    loop:  asyncio.AbstractEventLoop = asyncio.get_running_loop()
    queue: asyncio.Queue[str | None] = asyncio.Queue()

    def _run_sync() -> None:
        try:
            response = _client.models.generate_content_stream(
                model="gemini-2.0-flash",
                contents=message,
                config=types.GenerateContentConfig(system_instruction=system),
            )
            for chunk in response:
                if chunk.text:
                    loop.call_soon_threadsafe(queue.put_nowait, chunk.text)
        except Exception as exc:
            msg = str(exc)
            if "429" in msg or "RESOURCE_EXHAUSTED" in msg:
                loop.call_soon_threadsafe(queue.put_nowait, "\x00RATE_LIMIT")
            else:
                loop.call_soon_threadsafe(queue.put_nowait, f"\x00ERROR:{msg[:200]}")
        finally:
            loop.call_soon_threadsafe(queue.put_nowait, None)

    loop.run_in_executor(_executor, _run_sync)

    while True:
        token = await queue.get()
        if token is None:
            break
        yield token
