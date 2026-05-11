import json
from fastapi import APIRouter
from pydantic import BaseModel
from app.config import settings

router = APIRouter()

_NOTES_FILE = settings.data_dir / "notes.json"


def _read_notes() -> dict:
    if _NOTES_FILE.exists():
        try:
            return json.loads(_NOTES_FILE.read_text(encoding="utf-8-sig"))
        except Exception:
            return {}
    return {}


def _write_notes(notes: dict) -> None:
    _NOTES_FILE.write_text(json.dumps(notes, indent=2), encoding="utf-8")


class NoteBody(BaseModel):
    text: str


@router.get("/{course_id}/{module_index}")
def get_note(course_id: str, module_index: int):
    notes = _read_notes()
    key   = f"{course_id}/{module_index}"
    return {"text": notes.get(key, "")}


@router.post("/{course_id}/{module_index}")
def save_note(course_id: str, module_index: int, body: NoteBody):
    notes = _read_notes()
    key   = f"{course_id}/{module_index}"
    if body.text.strip():
        notes[key] = body.text
    else:
        notes.pop(key, None)
    _write_notes(notes)
    return {"ok": True}


@router.get("")
def list_notes():
    return _read_notes()


@router.get("/export")
def export_notes():
    """Return all notes as a single Markdown document."""
    notes = _read_notes()
    if not notes:
        return {"markdown": "# My Notes\n\n_No notes yet._\n"}
    lines = ["# My Notes\n"]
    for key, text in sorted(notes.items()):
        parts = key.split("/")
        course_id = parts[0]
        module    = parts[1] if len(parts) > 1 else "?"
        lines.append(f"## {course_id.replace('-', ' ').title()} — Module {int(module) + 1}\n")
        lines.append(text.strip())
        lines.append("")
    return {"markdown": "\n".join(lines)}
