import json
from pathlib import Path
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.config import settings

router = APIRouter()


def _courses_dir() -> Path:
    return settings.content_dir / "courses"


@router.get("")
def list_courses():
    base = _courses_dir()
    if not base.exists():
        return []
    courses = []
    for meta_file in sorted(base.glob("*/meta.json")):
        data = json.loads(meta_file.read_text(encoding="utf-8"))
        cdir = meta_file.parent
        data["id"] = cdir.name
        data["module_count"] = sum(
            1 for f in cdir.iterdir()
            if f.suffix in (".md", ".json") and f.name != "meta.json"
        )
        courses.append(data)
    return courses


@router.get("/{course_id}")
def get_course(course_id: str):
    base = _courses_dir() / course_id
    if not base.exists():
        raise HTTPException(status_code=404, detail="Course not found")

    meta_file = base / "meta.json"
    meta = json.loads(meta_file.read_text(encoding="utf-8")) if meta_file.exists() else {}

    # Collect ordered modules: markdown files and MCQ JSON files
    modules = []
    for f in sorted(base.iterdir()):
        if f.suffix == ".md":
            modules.append({"type": "lesson", "file": f.name, "content": f.read_text(encoding="utf-8")})
        elif f.suffix == ".json" and f.name != "meta.json":
            modules.append({"type": "mcq", "file": f.name, "content": json.loads(f.read_text(encoding="utf-8"))})

    return {"id": course_id, "meta": meta, "modules": modules}


class ProgressUpdate(BaseModel):
    module_index: int
    completed: bool


@router.post("/{course_id}/progress")
def update_course_progress(course_id: str, update: ProgressUpdate):
    progress_file = settings.data_dir / "progress.json"
    progress = json.loads(progress_file.read_text(encoding="utf-8")) if progress_file.exists() else {}

    course_progress = progress.setdefault("course_progress", {}).setdefault(course_id, {})
    course_progress[str(update.module_index)] = update.completed

    # Mark course completed if all modules done
    course = get_course(course_id)
    total = len(course["modules"])
    done  = sum(1 for v in course_progress.values() if v)
    if done >= total and course_id not in progress.get("completed_courses", []):
        progress.setdefault("completed_courses", []).append(course_id)

    progress_file.write_text(json.dumps(progress, indent=2), encoding="utf-8")
    return {"ok": True}
