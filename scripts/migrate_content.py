"""
Migrate legacy Streamlit content ->new content/ structure.

Run from the project root:
    python scripts/migrate_content.py

Output:
    content/courses/{slug}/meta.json
    content/courses/{slug}/*.md
    content/courses/{slug}/*.json   (MCQ)
    content/mcq/{topic}.json        (standalone practice MCQ)
    content/problems/problems.json  (coding problems)
"""

import json
import re
import shutil
from pathlib import Path

ROOT   = Path(__file__).resolve().parent.parent
LEGACY = ROOT / "_legacy" / "Static_Files"
DEST   = ROOT / "content"

# ──────────────────────────────────────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────────────────────────────────────

def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    return text.strip("-")


def topic_tags(title: str) -> list[str]:
    t = title.lower()
    mapping = {
        "dsa":          ["dsa", "algorithms"],
        "programming":  ["python", "programming", "fundamentals"],
        "array":        ["arrays", "data structures"],
        "linked":       ["linked lists", "data structures"],
        "stack":        ["stacks", "data structures"],
        "queue":        ["queues", "data structures"],
        "tree":         ["trees", "data structures"],
        "graph":        ["graphs", "data structures"],
        "hash":         ["hash maps", "data structures"],
        "heap":         ["heaps", "data structures"],
        "sort":         ["sorting", "algorithms"],
        "bubble":       ["sorting", "algorithms"],
        "insertion":    ["sorting", "algorithms"],
        "selection":    ["sorting", "algorithms"],
        "merge":        ["sorting", "algorithms"],
        "quick":        ["sorting", "algorithms"],
        "radix":        ["sorting", "algorithms"],
        "search":       ["searching", "algorithms"],
        "binary":       ["searching", "algorithms"],
        "linear":       ["searching", "algorithms"],
    }
    for key, tags in mapping.items():
        if key in t:
            return tags
    return ["dsa"]


def difficulty(title: str) -> str:
    t = title.lower()
    if any(k in t for k in ["intro", "fundamental", "array", "stack", "queue", "linked"]):
        return "beginner"
    if any(k in t for k in ["tree", "graph", "hash", "heap", "sort", "search"]):
        return "intermediate"
    return "beginner"


def find_file_ci(folder: Path, name: str) -> Path | None:
    """Case-insensitive file find — needed for mixed-case legacy paths."""
    for f in folder.iterdir():
        if f.name.lower() == name.lower():
            return f
    return None


def find_subdir_ci(parent: Path, name: str) -> Path | None:
    """Case-insensitive subdirectory find."""
    for d in parent.iterdir():
        if d.is_dir() and d.name.lower() == name.lower():
            return d
    return None


# ──────────────────────────────────────────────────────────────────────────────
# 1. Migrate courses
# ──────────────────────────────────────────────────────────────────────────────

def migrate_courses():
    learn_root = LEGACY / "Learn_Page"
    if not learn_root.exists():
        print("  [skip] _legacy/Static_Files/Learn_Page not found")
        return

    seen_slugs: set[str] = set()

    for box_dir in sorted(learn_root.iterdir()):
        if not box_dir.is_dir() or not box_dir.name.startswith("Image Box"):
            continue

        # Read meta JSON
        meta_file = box_dir / f"{box_dir.name}.json"
        if not meta_file.exists():
            continue

        try:
            meta = json.loads(meta_file.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"  [warn] could not parse {meta_file}: {e}")
            continue

        title = meta.get("title", box_dir.name)
        slug  = slugify(title)

        # Skip exact duplicates (same slug = same course content)
        if slug in seen_slugs:
            print(f"  [skip] duplicate: {title}")
            continue
        seen_slugs.add(slug)

        course_dest = DEST / "courses" / slug
        course_dest.mkdir(parents=True, exist_ok=True)

        # Write meta.json
        (course_dest / "meta.json").write_text(
            json.dumps({
                "title":       title,
                "description": f"Learn {title} with interactive lessons and quizzes.",
                "difficulty":  difficulty(title),
                "topics":      topic_tags(title),
            }, indent=2),
            encoding="utf-8",
        )

        # Find course-markdown subdirectory (case-insensitive)
        md_dir  = find_subdir_ci(box_dir, "Course Markdown File")
        mcq_dir = find_subdir_ci(box_dir, "Test Json File") or find_subdir_ci(box_dir, "Test JSON File")

        md_files  = sorted(md_dir.glob("*.md"))  if md_dir  and md_dir.exists()  else []
        mcq_files = sorted(mcq_dir.glob("*.json")) if mcq_dir and mcq_dir.exists() else []

        # Copy lessons — name as 01-lesson.md, 02-lesson.md …
        for i, src in enumerate(md_files, start=1):
            dst = course_dest / f"{i:02d}-{slugify(src.stem)}.md"
            shutil.copy2(src, dst)

        # Copy and normalise MCQ files — name as quiz-01.json …
        lesson_count = len(md_files)
        for i, src in enumerate(mcq_files, start=1):
            try:
                raw = json.loads(src.read_text(encoding="utf-8"))
            except Exception:
                continue

            questions = raw.get("questions", [])
            normalised = []
            for qi, q in enumerate(questions):
                normalised.append({
                    "id":       f"{slug}-q{qi+1}",
                    "topic":    topic_tags(title)[0],
                    "question": q.get("question", ""),
                    "options":  q.get("options", []),
                    "answer":   q.get("answer", ""),
                    "explanation": q.get("explanation", ""),
                    "incorrect_explanations": q.get("incorrect_explanation", {}),
                })

            dst = course_dest / f"{lesson_count + i:02d}-quiz.json"
            dst.write_text(json.dumps({"questions": normalised}, indent=2), encoding="utf-8")

        print(f"  [ok] {title} ->courses/{slug}/ ({len(md_files)} lessons, {len(mcq_files)} quizzes)")


# ──────────────────────────────────────────────────────────────────────────────
# 2. Migrate standalone MCQ practice tests
# ──────────────────────────────────────────────────────────────────────────────

def migrate_practice_mcq():
    test_root = LEGACY / "Practice_Page" / "All_Courses_Test"
    mcq_dest  = DEST / "mcq"
    mcq_dest.mkdir(parents=True, exist_ok=True)

    if not test_root.exists():
        print("  [skip] Practice_Page/All_Courses_Test not found")
        return

    for src in sorted(test_root.glob("*.json")):
        try:
            raw = json.loads(src.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"  [warn] {src.name}: {e}")
            continue

        questions = raw.get("questions", [])
        topic     = slugify(src.stem.split("_000")[0])

        normalised = []
        for qi, q in enumerate(questions):
            normalised.append({
                "id":       f"{topic}-q{qi+1}",
                "topic":    topic,
                "question": q.get("question", ""),
                "options":  q.get("options", []),
                "answer":   q.get("answer", ""),
                "explanation": q.get("explanation", ""),
                "incorrect_explanations": q.get("incorrect_explanation", {}),
            })

        dst_data = {
            "id":        src.stem,
            "title":     src.stem.split("_000")[0].replace("_", " "),
            "topic":     topic,
            "questions": normalised,
        }
        dst = mcq_dest / f"{topic}.json"
        dst.write_text(json.dumps(dst_data, indent=2), encoding="utf-8")
        print(f"  [ok] {src.name} ->mcq/{topic}.json ({len(normalised)} questions)")


# ──────────────────────────────────────────────────────────────────────────────
# 3. Migrate coding problems
# ──────────────────────────────────────────────────────────────────────────────

TOPIC_MAP = {
    "prob_arr": ["arrays"],
    "prob_str": ["strings"],
    "prob_BIM": ["bit manipulation"],
}


def infer_topics(problem_id: str) -> list[str]:
    for prefix, tags in TOPIC_MAP.items():
        if problem_id.startswith(prefix):
            return tags
    return ["algorithms"]


def migrate_problems():
    src_file = LEGACY / "Practice_Page_Problems" / "Coding_Problem.json"
    if not src_file.exists():
        print("  [skip] Coding_Problem.json not found")
        return

    raw       = json.loads(src_file.read_text(encoding="utf-8"))
    problems  = raw.get("problems", {})
    desc_root = LEGACY / "Practice_Page_Problems" / "problem_description"

    output = []
    for pid, data in problems.items():
        # Read description markdown
        desc_md = ""
        desc_path_str = data.get("Problem_Description", "")
        if desc_path_str:
            # Strip leading "Static_Files\\" prefix and find in legacy
            rel = Path(desc_path_str.replace("Static_Files\\", "").replace("Static_Files/", ""))
            abs_path = LEGACY / rel.relative_to(rel.parts[0]) if rel.parts[0] in ("Practice_Page_Problems", "Learn_Page") else LEGACY / rel
            # Fallback: look directly in desc_root
            if not abs_path.exists():
                abs_path = desc_root / rel.name
            if abs_path.exists():
                desc_md = abs_path.read_text(encoding="utf-8")

        # Normalise test cases: legacy format is [input_str, expected_str]
        raw_tests = data.get("Test_Cases", [])
        test_cases = []
        for i, tc in enumerate(raw_tests):
            if isinstance(tc, list) and len(tc) == 2:
                test_cases.append({"id": i + 1, "input": tc[0], "expected": tc[1]})

        output.append({
            "id":          pid,
            "title":       data.get("title", pid),
            "difficulty":  data.get("Difficulty", "Easy").lower(),
            "topics":      infer_topics(pid),
            "description": desc_md or data.get("title", ""),
            "starter_code": "# Write your solution here\n",
            "test_cases":  test_cases,
        })

    dest = DEST / "problems" / "problems.json"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(output, indent=2), encoding="utf-8")
    print(f"  [ok] {len(output)} coding problems ->problems/problems.json")


# ──────────────────────────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("\n=== Migrating courses ===")
    migrate_courses()

    print("\n=== Migrating practice MCQ tests ===")
    migrate_practice_mcq()

    print("\n=== Migrating coding problems ===")
    migrate_problems()

    print("\nDone. Content is in content/")
