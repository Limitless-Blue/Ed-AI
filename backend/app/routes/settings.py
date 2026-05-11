import json
from fastapi import APIRouter, BackgroundTasks
from app.config import settings
from app.routes.progress import write_progress, _defaults

router = APIRouter()

_INTERVIEW_FILE = settings.data_dir / "interview_history.json"
_SR_FILE        = settings.data_dir / "sr.json"
_NOTES_FILE     = settings.data_dir / "notes.json"


@router.get("/status")
def get_status():
    """Return basic platform status info."""
    return {
        "api_model":          "gemini-2.0-flash",
        "rag_enabled":        (settings.chroma_dir / "chroma.sqlite3").exists(),
        "content_courses":    len(list((settings.content_dir / "courses").glob("*/meta.json")))
                              if (settings.content_dir / "courses").exists() else 0,
        "content_problems":   _count_problems(),
        "content_mcq_tests":  len(list((settings.content_dir / "mcq").glob("*.json")))
                              if (settings.content_dir / "mcq").exists() else 0,
    }


def _count_problems() -> int:
    f = settings.content_dir / "problems" / "problems.json"
    if not f.exists():
        return 0
    try:
        return len(json.loads(f.read_text(encoding="utf-8-sig")))
    except Exception:
        return 0


@router.post("/reset/progress")
def reset_progress():
    write_progress(dict(_defaults))
    return {"ok": True}


@router.post("/reset/interview")
def reset_interview_history():
    if _INTERVIEW_FILE.exists():
        _INTERVIEW_FILE.write_text("[]", encoding="utf-8")
    return {"ok": True}


@router.post("/reset/spaced-repetition")
def reset_sr():
    if _SR_FILE.exists():
        _SR_FILE.write_text("{}", encoding="utf-8")
    return {"ok": True}


@router.post("/reset/notes")
def reset_notes():
    if _NOTES_FILE.exists():
        _NOTES_FILE.write_text("{}", encoding="utf-8")
    return {"ok": True}


@router.post("/reset/all")
def reset_all():
    reset_progress()
    reset_interview_history()
    reset_sr()
    reset_notes()
    return {"ok": True}


# ---------------------------------------------------------------------------
# RAG re-indexing
# ---------------------------------------------------------------------------

def _index_all_courses() -> None:
    """Background task: rebuild Chroma stores for every course directory."""
    from app.services.rag import _get_store
    courses_dir = settings.content_dir / "courses"
    if not courses_dir.exists():
        return
    for d in sorted(courses_dir.iterdir()):
        if d.is_dir():
            try:
                _get_store(d.name)
            except Exception:
                pass


@router.post("/reindex")
async def reindex_content(background_tasks: BackgroundTasks):
    """Clear RAG cache and re-embed all course content in the background."""
    from app.services import rag as rag_module
    rag_module._stores.clear()
    background_tasks.add_task(_index_all_courses)
    return {"ok": True, "message": "Re-indexing started in background."}
