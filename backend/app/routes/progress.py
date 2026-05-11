import json
from datetime import date, timedelta
from pathlib import Path

from fastapi import APIRouter
from app.config import settings

router = APIRouter()

PROGRESS_FILE = settings.data_dir / "progress.json"

_defaults: dict = {
    "topics": {},
    "completed_courses": [],
    "completed_problems": [],
    "completed_mcqs": [],
    "course_progress": {},
    "daily_activity": {},  # { "YYYY-MM-DD": { "problems": 0, "mcqs": 0, "messages": 0 } }
}


def read_progress() -> dict:
    if not PROGRESS_FILE.exists():
        return dict(_defaults)
    return json.loads(PROGRESS_FILE.read_text(encoding="utf-8-sig"))


def write_progress(progress: dict) -> None:
    PROGRESS_FILE.write_text(json.dumps(progress, indent=2), encoding="utf-8")


def record_activity(key: str, amount: int = 1) -> None:
    """Increment a daily activity counter (problems / mcqs / messages)."""
    progress = read_progress()
    today = str(date.today())
    day = progress.setdefault("daily_activity", {}).setdefault(today, {"problems": 0, "mcqs": 0, "messages": 0})
    day[key] = day.get(key, 0) + amount
    write_progress(progress)


def _streak(daily: dict) -> int:
    """Count consecutive days with any activity, ending today or yesterday."""
    if not daily:
        return 0
    today = date.today()
    streak = 0
    d = today
    # Accept streak starting today or yesterday (so a morning user isn't penalised)
    if str(d) not in daily and str(d - timedelta(days=1)) not in daily:
        return 0
    if str(d) not in daily:
        d = d - timedelta(days=1)
    while str(d) in daily:
        streak += 1
        d -= timedelta(days=1)
    return streak


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@router.get("")
def get_progress():
    p = read_progress()
    p.setdefault("daily_activity", {})
    return p


@router.get("/stats")
def get_stats():
    """Aggregated stats for the dashboard: streak, 7-day activity, topic summary."""
    p = read_progress()
    daily = p.get("daily_activity", {})
    today = date.today()

    week = []
    for i in range(6, -1, -1):  # oldest to newest
        d = str(today - timedelta(days=i))
        entry = daily.get(d, {})
        week.append({
            "date":     d,
            "problems": entry.get("problems", 0),
            "mcqs":     entry.get("mcqs", 0),
            "messages": entry.get("messages", 0),
            "total":    entry.get("problems", 0) + entry.get("mcqs", 0) + entry.get("messages", 0),
        })

    topics = p.get("topics", {})
    weak   = [{"topic": t, **s} for t, s in topics.items() if s.get("accuracy", 1.0) < 0.6]
    strong = [{"topic": t, **s} for t, s in topics.items() if s.get("accuracy", 0.0) >= 0.8]

    return {
        "streak":             _streak(daily),
        "week":               week,
        "completed_courses":  len(p.get("completed_courses", [])),
        "completed_problems": len(p.get("completed_problems", [])),
        "completed_mcqs":     len(p.get("completed_mcqs", [])),
        "topics":             topics,
        "weak_topics":        sorted(weak,   key=lambda x: x["accuracy"]),
        "strong_topics":      sorted(strong, key=lambda x: -x["accuracy"]),
    }


@router.get("/recommendations")
def get_recommendations():
    """Return up to 3 recommended problems and courses based on weak topics."""
    p = read_progress()
    topics = p.get("topics", {})
    completed_problems = set(p.get("completed_problems", []))
    completed_courses  = set(p.get("completed_courses", []))

    # Weak topics sorted worst-first
    weak_topics = sorted(
        [t for t, s in topics.items() if s.get("accuracy", 1.0) < 0.7],
        key=lambda t: topics[t].get("accuracy", 1.0),
    )

    # --- Problems ---
    problems_file = settings.content_dir / "problems" / "problems.json"
    all_problems  = json.loads(problems_file.read_text(encoding="utf-8")) if problems_file.exists() else []

    rec_problems: list[dict] = []
    seen_ids: set[str] = set()

    # First pass: problems matching weak topics
    for topic in weak_topics:
        for p_item in all_problems:
            if p_item["id"] in completed_problems or p_item["id"] in seen_ids:
                continue
            if topic.lower() in [t.lower() for t in p_item.get("topics", [])]:
                rec_problems.append({
                    "id":         p_item["id"],
                    "title":      p_item["title"],
                    "difficulty": p_item.get("difficulty", ""),
                    "topics":     p_item.get("topics", []),
                    "reason":     f"Weak area: {topic}",
                })
                seen_ids.add(p_item["id"])
            if len(rec_problems) >= 3:
                break
        if len(rec_problems) >= 3:
            break

    # Fill up to 3 with any unsolved problems
    for p_item in all_problems:
        if len(rec_problems) >= 3:
            break
        if p_item["id"] in completed_problems or p_item["id"] in seen_ids:
            continue
        rec_problems.append({
            "id":         p_item["id"],
            "title":      p_item["title"],
            "difficulty": p_item.get("difficulty", ""),
            "topics":     p_item.get("topics", []),
            "reason":     "Not yet attempted",
        })
        seen_ids.add(p_item["id"])

    # --- Courses ---
    courses_dir = settings.content_dir / "courses"
    all_courses = []
    if courses_dir.exists():
        for meta_file in sorted(courses_dir.glob("*/meta.json")):
            data = json.loads(meta_file.read_text(encoding="utf-8"))
            data["id"] = meta_file.parent.name
            all_courses.append(data)

    rec_courses: list[dict] = []
    seen_course_ids: set[str] = set()

    for topic in weak_topics:
        for c in all_courses:
            if c["id"] in completed_courses or c["id"] in seen_course_ids:
                continue
            if topic.lower() in [t.lower() for t in c.get("topics", [])]:
                rec_courses.append({
                    "id":         c["id"],
                    "title":      c["title"],
                    "difficulty": c.get("difficulty", ""),
                    "reason":     f"Weak area: {topic}",
                })
                seen_course_ids.add(c["id"])
            if len(rec_courses) >= 3:
                break
        if len(rec_courses) >= 3:
            break

    for c in all_courses:
        if len(rec_courses) >= 3:
            break
        if c["id"] in completed_courses or c["id"] in seen_course_ids:
            continue
        rec_courses.append({
            "id":         c["id"],
            "title":      c["title"],
            "difficulty": c.get("difficulty", ""),
            "reason":     "Not yet started",
        })
        seen_course_ids.add(c["id"])

    return {"problems": rec_problems[:3], "courses": rec_courses[:3]}


@router.delete("")
def reset_progress():
    write_progress(dict(_defaults))
    return {"ok": True}
