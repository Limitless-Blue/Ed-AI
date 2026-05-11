import json
from datetime import date, timedelta
from pathlib import Path
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.config import settings
from app.services.executor import run_code
from app.routes.progress import record_activity

router = APIRouter()


# ──────────────────────────────────────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────────────────────────────────────

def _problems_file() -> Path:
    return settings.content_dir / "problems" / "problems.json"

def _mcq_dir() -> Path:
    return settings.content_dir / "mcq"

def _read_progress() -> dict:
    f = settings.data_dir / "progress.json"
    return json.loads(f.read_text(encoding="utf-8-sig")) if f.exists() else {}

def _write_progress(progress: dict) -> None:
    f = settings.data_dir / "progress.json"
    f.write_text(json.dumps(progress, indent=2), encoding="utf-8")

def _sr_file() -> Path:
    return settings.data_dir / "sr.json"

def _read_sr() -> dict:
    f = _sr_file()
    return json.loads(f.read_text(encoding="utf-8-sig")) if f.exists() else {}

def _write_sr(sr: dict) -> None:
    _sr_file().write_text(json.dumps(sr, indent=2), encoding="utf-8")


def _sm2(card: dict, correct: bool) -> dict:
    """Apply SM-2 algorithm and return updated card."""
    ef       = card.get("ef", 2.5)
    interval = card.get("interval", 1)
    reps     = card.get("reps", 0)

    q = 5 if correct else 1   # quality: 5=perfect, 1=wrong
    if correct:
        if reps == 0:
            interval = 1
        elif reps == 1:
            interval = 6
        else:
            interval = round(interval * ef)
        reps += 1
    else:
        interval = 1
        reps     = 0

    ef = max(1.3, ef + 0.1 - (5 - q) * (0.08 + (5 - q) * 0.02))
    due = str(date.today() + timedelta(days=interval))
    return {"ef": round(ef, 3), "interval": interval, "reps": reps, "due": due}


# ──────────────────────────────────────────────────────────────────────────────
# Coding problems
# ──────────────────────────────────────────────────────────────────────────────

@router.get("/problems")
def list_problems(topic: str | None = None, difficulty: str | None = None):
    f = _problems_file()
    if not f.exists():
        return []
    problems = json.loads(f.read_text(encoding="utf-8"))
    if topic:
        problems = [p for p in problems if topic.lower() in [t.lower() for t in p.get("topics", [])]]
    if difficulty:
        problems = [p for p in problems if p.get("difficulty", "").lower() == difficulty.lower()]
    # Strip description from list view (too large)
    return [{k: v for k, v in p.items() if k != "description"} for p in problems]


@router.get("/problems/{problem_id}")
def get_problem(problem_id: str):
    f = _problems_file()
    if not f.exists():
        raise HTTPException(status_code=404, detail="Problem bank not found")
    problems = json.loads(f.read_text(encoding="utf-8"))
    match = next((p for p in problems if p["id"] == problem_id), None)
    if not match:
        raise HTTPException(status_code=404, detail="Problem not found")
    return match


class SubmitRequest(BaseModel):
    problem_id: str
    source_code: str


@router.post("/submit")
def submit_code(req: SubmitRequest):
    problem    = get_problem(req.problem_id)
    test_cases = problem.get("test_cases", [])
    results    = run_code(req.source_code, test_cases)
    passed     = sum(1 for r in results if r["passed"])
    total      = len(results)

    record_activity("problems")
    if passed == total and total > 0:
        progress = _read_progress()
        if req.problem_id not in progress.get("completed_problems", []):
            progress.setdefault("completed_problems", []).append(req.problem_id)
        for topic in problem.get("topics", []):
            t = progress.setdefault("topics", {}).setdefault(topic, {"seen": 0, "correct": 0})
            t["seen"]    += 1
            t["correct"] += 1
            t["accuracy"] = t["correct"] / t["seen"]
        _write_progress(progress)

    return {
        "passed":  passed,
        "total":   total,
        "results": results,
        "status":  "accepted" if passed == total else "partial" if passed > 0 else "wrong",
    }


# ──────────────────────────────────────────────────────────────────────────────
# Standalone MCQ practice tests
# ──────────────────────────────────────────────────────────────────────────────

@router.get("/mcq")
def list_mcq_tests():
    d = _mcq_dir()
    if not d.exists():
        return []
    tests = []
    for f in sorted(d.glob("*.json")):
        data = json.loads(f.read_text(encoding="utf-8"))
        tests.append({
            "id":    data.get("id", f.stem),
            "title": data.get("title", f.stem),
            "topic": data.get("topic", f.stem),
            "count": len(data.get("questions", [])),
        })
    return tests


@router.get("/mcq/review")
def get_review_queue(limit: int = 20):
    """Return questions due for review today (SM-2 spaced repetition)."""
    sr      = _read_sr()
    today   = str(date.today())
    due_ids = {qid for qid, card in sr.items() if card.get("due", "0000-00-00") <= today}

    d = _mcq_dir()
    if not d.exists():
        return {"questions": [], "total_due": 0}

    questions = []
    for f in sorted(d.glob("*.json")):
        data = json.loads(f.read_text(encoding="utf-8-sig"))
        for q in data.get("questions", []):
            if q.get("id") in due_ids:
                questions.append({**q, "source_test": data.get("title", f.stem)})
            if len(questions) >= limit:
                break
        if len(questions) >= limit:
            break

    # Fill remaining slots with unseen questions
    if len(questions) < limit:
        seen_ids = set(sr.keys())
        for f in sorted(d.glob("*.json")):
            data = json.loads(f.read_text(encoding="utf-8-sig"))
            for q in data.get("questions", []):
                if q.get("id") not in seen_ids and q.get("id") not in due_ids:
                    questions.append({**q, "source_test": data.get("title", f.stem)})
                    seen_ids.add(q.get("id"))
                if len(questions) >= limit:
                    break
            if len(questions) >= limit:
                break

    return {"questions": questions, "total_due": len(due_ids)}


@router.get("/mcq/{test_id}")
def get_mcq_test(test_id: str):
    d = _mcq_dir()
    for f in d.glob("*.json"):
        data = json.loads(f.read_text(encoding="utf-8-sig"))
        if data.get("id") == test_id or f.stem == test_id:
            return data
    raise HTTPException(status_code=404, detail="MCQ test not found")


class MCQResultRequest(BaseModel):
    mcq_id:      str
    topic:       str
    correct:     bool
    question_id: str | None = None


@router.post("/mcq/result")
def record_mcq_result(req: MCQResultRequest):
    progress = _read_progress()
    t = progress.setdefault("topics", {}).setdefault(req.topic, {"seen": 0, "correct": 0})
    t["seen"]    += 1
    t["correct"] += 1 if req.correct else 0
    t["accuracy"] = t["correct"] / t["seen"]
    if req.correct and req.mcq_id not in progress.get("completed_mcqs", []):
        progress.setdefault("completed_mcqs", []).append(req.mcq_id)
    _write_progress(progress)
    record_activity("mcqs")

    # Update spaced repetition card for this question
    if req.question_id:
        sr = _read_sr()
        card = sr.get(req.question_id, {})
        sr[req.question_id] = _sm2(card, req.correct)
        _write_sr(sr)

    return {"ok": True}
