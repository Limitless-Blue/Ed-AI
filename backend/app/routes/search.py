import json
from pathlib import Path
from fastapi import APIRouter
from app.config import settings

router = APIRouter()


def _snippet(text: str, query: str, radius: int = 120) -> str:
    lower = text.lower()
    idx   = lower.find(query.lower())
    if idx == -1:
        return text[:radius].strip() + "…"
    start = max(0, idx - radius // 2)
    end   = min(len(text), idx + radius // 2)
    snip  = text[start:end].strip()
    if start > 0:
        snip = "…" + snip
    if end < len(text):
        snip = snip + "…"
    return snip


@router.get("")
def search(q: str):
    if not q or len(q.strip()) < 2:
        return {"results": []}

    term    = q.strip().lower()
    results = []

    # ── Courses (search title + markdown content) ──────────────────────────
    courses_dir = settings.content_dir / "courses"
    if courses_dir.exists():
        for meta_file in sorted(courses_dir.glob("*/meta.json")):
            meta      = json.loads(meta_file.read_text(encoding="utf-8-sig"))
            course_id = meta_file.parent.name
            title     = meta.get("title", course_id)

            # Title match (high priority)
            if term in title.lower() or any(term in t.lower() for t in meta.get("topics", [])):
                results.append({
                    "type":    "course",
                    "id":      course_id,
                    "title":   title,
                    "snippet": meta.get("description", ""),
                    "score":   2,
                })
                continue

            # Content match (scan lesson markdown)
            for md in meta_file.parent.glob("*.md"):
                content = md.read_text(encoding="utf-8-sig")
                if term in content.lower():
                    results.append({
                        "type":    "course",
                        "id":      course_id,
                        "title":   title,
                        "snippet": _snippet(content, q),
                        "score":   1,
                    })
                    break

    # ── Coding problems ────────────────────────────────────────────────────
    problems_file = settings.content_dir / "problems" / "problems.json"
    if problems_file.exists():
        problems = json.loads(problems_file.read_text(encoding="utf-8-sig"))
        for p in problems:
            title = p.get("title", "")
            if (term in title.lower()
                    or any(term in t.lower() for t in p.get("topics", []))
                    or term in p.get("description", "").lower()):
                results.append({
                    "type":       "problem",
                    "id":         p["id"],
                    "title":      title,
                    "snippet":    _snippet(p.get("description", title), q),
                    "difficulty": p.get("difficulty", ""),
                    "score":      2 if term in title.lower() else 1,
                })

    # ── MCQ tests ──────────────────────────────────────────────────────────
    mcq_dir = settings.content_dir / "mcq"
    if mcq_dir.exists():
        for f in sorted(mcq_dir.glob("*.json")):
            data  = json.loads(f.read_text(encoding="utf-8-sig"))
            title = data.get("title", f.stem)
            topic = data.get("topic", "")
            if term in title.lower() or term in topic.lower():
                results.append({
                    "type":    "mcq",
                    "id":      data.get("id", f.stem),
                    "title":   title,
                    "snippet": f"{len(data.get('questions', []))} questions · {topic}",
                    "score":   1,
                })
                continue
            # Search question text
            for qitem in data.get("questions", []):
                if term in qitem.get("question", "").lower():
                    results.append({
                        "type":    "mcq",
                        "id":      data.get("id", f.stem),
                        "title":   title,
                        "snippet": _snippet(qitem["question"], q),
                        "score":   1,
                    })
                    break

    results.sort(key=lambda r: -r["score"])
    return {"results": results[:12]}
