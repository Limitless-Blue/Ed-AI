"""
Mock interview route — text + audio input, debrief generation.
"""

import asyncio
import base64
import json
from concurrent.futures import ThreadPoolExecutor

from google import genai
from google.genai import types
from fastapi import APIRouter, Body
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from app.config import settings

router    = APIRouter()
_executor = ThreadPoolExecutor(max_workers=2)
_client   = genai.Client(api_key=settings.google_api_key)

_HISTORY_FILE = settings.data_dir / "interview_history.json"


def _load_history() -> list[dict]:
    if _HISTORY_FILE.exists():
        try:
            return json.loads(_HISTORY_FILE.read_text(encoding="utf-8-sig"))
        except Exception:
            return []
    return []


def _save_history(history: list[dict]) -> None:
    _HISTORY_FILE.write_text(json.dumps(history, indent=2), encoding="utf-8")


PERSONAS: dict[str, str] = {
    "technical": (
        "You are a senior software engineer conducting a technical coding interview. "
        "Ask one DSA or system-design question at a time. Probe depth, not just correctness. "
        "Acknowledge the candidate's answer briefly before asking the next question."
    ),
    "hr": (
        "You are an experienced HR interviewer conducting a behavioural interview. "
        "Use the STAR method. Ask about past experiences, teamwork, and conflict resolution. "
        "Ask one question at a time. Be warm but professional."
    ),
    "system_design": (
        "You are a principal engineer conducting a system design interview. "
        "Present one open-ended system design problem (e.g., design a URL shortener, design Twitter). "
        "Guide the candidate through requirements, high-level architecture, data models, "
        "scalability, and trade-offs. Ask clarifying follow-ups to probe depth. "
        "Never give the answer — drive the conversation with questions."
    ),
    "behavioral": (
        "You are a senior engineering manager running a behavioural and leadership interview. "
        "Ask situational questions focused on leadership, conflict resolution, ambiguity, "
        "cross-functional collaboration, and growth mindset. "
        "Use the STAR framework. Ask one question at a time. "
        "Follow up to draw out specifics and lessons learned."
    ),
}

_history: list[dict] = _load_history()


def _to_sdk_contents(history: list[dict]) -> list[types.Content]:
    contents = []
    for turn in history:
        parts = [types.Part(text=p) for p in turn["parts"] if isinstance(p, str)]
        contents.append(types.Content(role=turn["role"], parts=parts))
    return contents


# ── Models ─────────────────────────────────────────────────────────────────

class InterviewMessage(BaseModel):
    message:        str
    interview_type: str       = "technical"
    topics:         list[str] = []
    difficulty:     str       = "medium"


# ── Routes ─────────────────────────────────────────────────────────────────

@router.post("/message")
async def interview_message(req: InterviewMessage):
    global _history

    system = PERSONAS.get(req.interview_type, PERSONAS["technical"])
    if req.topics:
        system += f" Focus on these topics: {', '.join(req.topics)}."
    system += f" Difficulty: {req.difficulty}."

    _history.append({"role": "user", "parts": [req.message]})
    history_snapshot = list(_history)

    loop:  asyncio.AbstractEventLoop = asyncio.get_running_loop()
    queue: asyncio.Queue[str | None] = asyncio.Queue()
    full_response: list[str]         = []

    def _run_sync() -> None:
        try:
            contents = _to_sdk_contents(history_snapshot)
            response = _client.models.generate_content_stream(
                model="gemini-2.0-flash",
                contents=contents,
                config=types.GenerateContentConfig(system_instruction=system),
            )
            for chunk in response:
                if chunk.text:
                    full_response.append(chunk.text)
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

    async def event_stream():
        while True:
            token = await queue.get()
            if token is None:
                if full_response:
                    _history.append({"role": "model", "parts": ["".join(full_response)]})
                    _save_history(_history)
                yield "data: [DONE]\n\n"
                break
            yield f"data: {json.dumps({'token': token})}\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")


@router.post("/transcribe")
async def transcribe_audio(
    audio_b64: str  = Body(..., embed=True),
    mime_type: str  = Body("audio/webm", embed=True),
):
    """Transcribe a base64-encoded audio blob using Gemini."""
    loop:  asyncio.AbstractEventLoop = asyncio.get_running_loop()
    queue: asyncio.Queue[str | None] = asyncio.Queue()

    def _run_sync() -> None:
        try:
            audio_bytes = base64.b64decode(audio_b64)
            response = _client.models.generate_content(
                model="gemini-2.0-flash",
                contents=[
                    types.Part(
                        inline_data=types.Blob(mime_type=mime_type, data=audio_bytes)
                    ),
                    types.Part(
                        text="Transcribe the speech in this audio accurately. "
                             "Return only the spoken words, nothing else."
                    ),
                ],
            )
            loop.call_soon_threadsafe(queue.put_nowait, response.text.strip())
        except Exception as exc:
            loop.call_soon_threadsafe(queue.put_nowait, f"[Transcription error: {exc}]")
        finally:
            loop.call_soon_threadsafe(queue.put_nowait, None)

    loop.run_in_executor(_executor, _run_sync)
    text = await queue.get()
    await queue.get()  # drain sentinel
    return {"text": text or ""}


@router.post("/debrief")
async def get_debrief():
    """Generate a structured debrief of the current interview session."""
    if not _history:
        return {"debrief": "No interview history to debrief yet."}

    transcript_lines = []
    for turn in _history:
        role = "Candidate" if turn["role"] == "user" else "Interviewer"
        text = " ".join(turn["parts"])
        transcript_lines.append(f"{role}: {text}")
    transcript = "\n\n".join(transcript_lines)

    prompt = (
        "You are an expert interview coach. Review this mock interview transcript "
        "and give a structured, actionable debrief.\n\n"
        f"TRANSCRIPT:\n{transcript}\n\n"
        "Write the debrief in Markdown with these sections:\n"
        "## Overall Performance\n"
        "## Strengths\n"
        "## Areas to Improve\n"
        "## Topics to Study\n"
        "## Score (out of 10)\n\n"
        "Be specific and constructive. Reference actual moments from the transcript."
    )

    loop:  asyncio.AbstractEventLoop = asyncio.get_running_loop()
    queue: asyncio.Queue[str | None] = asyncio.Queue()

    def _run_sync() -> None:
        try:
            response = _client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt,
            )
            loop.call_soon_threadsafe(queue.put_nowait, response.text)
        except Exception as exc:
            loop.call_soon_threadsafe(
                queue.put_nowait, f"[Debrief error: {exc}]"
            )
        finally:
            loop.call_soon_threadsafe(queue.put_nowait, None)

    loop.run_in_executor(_executor, _run_sync)
    text = await queue.get()
    await queue.get()
    return {"debrief": text or ""}


@router.post("/reset")
def reset_interview():
    global _history
    _history = []
    _save_history(_history)
    return {"ok": True}
