# Ed-AI

An AI-powered technical education platform. Learn DSA and programming through structured courses, solve coding problems in a sandboxed editor, practise MCQ tests with spaced repetition, and sharpen interview skills with a streaming AI interviewer — all guided by a Socratic tutor that knows exactly what you are working on.

---

## Table of Contents

1. [Tech Stack](#tech-stack)
2. [Project Structure](#project-structure)
3. [Prerequisites](#prerequisites)
4. [Setup](#setup)
5. [Running the App](#running-the-app)
6. [Feature Guide](#feature-guide)
   - [Learn](#learn)
   - [Practice — Coding Problems](#practice--coding-problems)
   - [Practice — MCQ Tests](#practice--mcq-tests)
   - [Practice — Spaced Repetition Review](#practice--spaced-repetition-review)
   - [Mock Interview](#mock-interview)
   - [Dashboard](#dashboard)
   - [AI Tutor Sidebar](#ai-tutor-sidebar)
   - [Search](#search)
   - [Settings](#settings)
7. [Keyboard Shortcuts](#keyboard-shortcuts)
8. [Adding Your Own Content](#adding-your-own-content)
9. [API Reference](#api-reference)
10. [How the AI Tutor Works](#how-the-ai-tutor-works)
11. [Troubleshooting](#troubleshooting)

---

## Tech Stack

| Layer       | Technology                                          |
|-------------|-----------------------------------------------------|
| Frontend    | React 18 · TypeScript · Vite · Tailwind CSS         |
| Code editor | Monaco Editor (VS Code engine)                      |
| Backend     | FastAPI · Python 3.11+                              |
| AI          | Google Gemini 2.0 Flash (`google-genai` SDK)        |
| RAG         | Chroma · Gemini `embedding-001`                     |
| Storage     | Flat JSON files in `data/` — no database required   |

---

## Project Structure

```
Ed-AI/
├── backend/
│   └── app/
│       ├── main.py              Entry point, CORS, router registration
│       ├── config.py            Reads root .env; exposes paths
│       ├── routes/
│       │   ├── tutor.py         POST /tutor/message  (SSE stream)
│       │   ├── courses.py       GET /courses, progress tracking
│       │   ├── practice.py      Problems, MCQ, spaced repetition
│       │   ├── interview.py     Streaming interview + transcription + debrief
│       │   ├── progress.py      Stats, recommendations, activity
│       │   ├── notes.py         Per-lesson notes, export
│       │   ├── search.py        Full-text search across all content
│       │   └── settings.py      Platform status, reindex, data resets
│       └── services/
│           ├── tutor.py         Prompt assembly, RAG retrieval, streaming
│           ├── rag.py           Chroma store + Gemini embeddings wrapper
│           └── executor.py      Sandboxed Python code runner
│
├── frontend/
│   └── src/
│       ├── pages/
│       │   ├── LearnPage.tsx         Courses, progress bars, notes
│       │   ├── PracticePage.tsx      Problems + MCQ + Review tabs
│       │   ├── InterviewPage.tsx     Chat + audio + debrief
│       │   ├── DashboardPage.tsx     Stats, badges, recommendations
│       │   └── SettingsPage.tsx      Status, reindex, resets, export
│       ├── components/
│       │   ├── TutorSidebar/         Streaming AI chat panel
│       │   ├── CodeEditor/           Monaco editor + test runner
│       │   ├── MCQQuiz/              Quiz engine + SR tracking
│       │   ├── SearchModal/          ⌘K command palette
│       │   ├── OnboardingModal/      First-run walkthrough
│       │   └── KeyboardShortcutsModal/
│       ├── sounds.ts                 Web Audio API sound effects (no files needed)
│       ├── store.ts                  Zustand — tutor context + mode
│       └── api.ts                    fetch helpers, SSE parser
│
├── content/
│   ├── courses/      One folder per course (markdown lessons + MCQ JSON)
│   ├── mcq/          Standalone MCQ test banks
│   └── problems/
│       └── problems.json
│
├── data/             Auto-created at runtime — gitignored except .gitkeep
│   ├── .gitkeep          Ensures this directory exists on fresh clones
│   ├── progress.json     User progress (gitignored)
│   ├── notes.json        Lesson notes (gitignored)
│   ├── sr.json           Spaced repetition cards (gitignored)
│   ├── interview_history.json  (gitignored)
│   └── chroma/           RAG vector store (gitignored)
│
├── .env              Your API key — copy from .env.example (gitignored)
├── .env.example      Template — safe to commit
└── backend/requirements.txt
```

---

## Prerequisites

| Tool | Version | Download |
|------|---------|----------|
| Python | 3.11 or newer | [python.org](https://www.python.org/downloads/) |
| Node.js | 20 or newer | [nodejs.org](https://nodejs.org/) |
| Gemini API key | Free tier available | [aistudio.google.com/apikey](https://aistudio.google.com/apikey) |

---

## Setup

### 1 — Clone the repo

```bash
git clone https://github.com/pvchaitanya8/Ed-AI.git
cd Ed-AI
```

### 2 — Add your Gemini API key

```bash
# Windows
copy .env.example .env

# macOS / Linux
cp .env.example .env
```

Open `.env` and fill in your key:

```
GOOGLE_API_KEY=AIzaSy...your-key-here...
```

Get a free key at [aistudio.google.com/apikey](https://aistudio.google.com/apikey). The free tier is sufficient for development.

### 3 — Install backend dependencies

```bash
python -m venv venv

# Activate — Windows
venv\Scripts\activate

# Activate — macOS / Linux
source venv/bin/activate

pip install -r backend/requirements.txt
```

### 4 — Install frontend dependencies

```bash
cd frontend
npm install
cd ..
```

That's it. No database setup, no migrations, no Docker required. The `data/` directory already exists in the repo (via `.gitkeep`) and all runtime JSON files are created automatically on first use.

---

## Running the App

You need **two terminals** running simultaneously.

**Terminal 1 — Backend:**

```bash
# Make sure your venv is active first
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS / Linux

cd backend
uvicorn app.main:app --reload --port 8000
```

Expected output:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

**Terminal 2 — Frontend:**

```bash
cd frontend
npm run dev
```

Expected output:
```
  VITE v5.x  ready in ...ms
  ➜  Local:   http://localhost:5173/
```

Open **[http://localhost:5173](http://localhost:5173)** in your browser.

On first launch you will see a short onboarding walkthrough. Press **Skip** or click through it to reach the app.

### First-time: Index content for the AI Tutor

The AI tutor uses RAG to pull relevant course material into context. Trigger indexing once after setup:

1. Go to **Settings** (left nav)
2. Click **Re-index** under "Content & RAG"
3. Indexing runs in the background — a few minutes depending on API quota

The tutor still works without indexing; it just won't reference specific course content.

---

## Feature Guide

### Learn

Navigate to **Learn** in the left sidebar.

- Browse all available courses — each card shows difficulty, topics, and a **progress bar** (modules completed / total).
- Click a course to open it. Use the **module tabs** at the top to jump between lessons and quizzes. Completed modules show a ✓ checkmark.
- At the bottom of each lesson is a **Notes** panel. Notes save automatically with an 800 ms debounce. A "Saved" indicator confirms persistence.
- Use **Previous / Next Module** to move through the course, or click **Complete Course** on the last module.

**Tip:** Use **⌘K** (or **Ctrl+K**) to search for a specific course by name and jump straight into it.

---

### Practice — Coding Problems

Navigate to **Practice → Coding** tab.

- Browse all problems in the table. Filter visually by difficulty colour: green = easy, yellow = medium, red = hard.
- Click a problem to open the split-panel editor:
  - **Left panel** — problem description with constraints and examples.
  - **Right panel** — Monaco editor (full VS Code engine) with syntax highlighting and tab support. Language is Python 3.
- Write your solution and click **Run Code**.
- The test runner shows each test case: passed (green) or failed (red) with expected vs actual output.
- Passing all tests marks the problem as solved and updates your topic accuracy on the Dashboard.

**Sandbox safety:** Code runs in an isolated subprocess. Imports of `os`, `subprocess`, `socket`, `pathlib`, `ctypes`, and similar modules are blocked. Execution is killed after 5 seconds.

---

### Practice — MCQ Tests

Navigate to **Practice → MCQ Tests** tab.

- Browse test banks by topic (Arrays, Linked Lists, Trees, Sorting, etc.).
- Click a test bank to start a quiz.
- Each question shows 4 options. After answering, you see the explanation (and per-option explanations for wrong answers where available).
- Results are recorded to your topic accuracy profile on the Dashboard.
- Every question answered is scheduled for spaced-repetition review automatically.

---

### Practice — Spaced Repetition Review

Navigate to **Practice → Review** tab.

- The red badge on the tab shows how many questions are due today.
- Click **Start Review Session** to work through due questions.
- The SM-2 algorithm adjusts each card's next review date based on correctness:
  - Correct → interval grows (1 → 6 → increasing multiplier days)
  - Wrong → resets to 1-day review
- Come back daily to maintain your streak and keep recall sharp.

---

### Mock Interview

Navigate to **Interview** in the left sidebar.

**Setup:**
1. Choose an interview type: **Technical** · **System Design** · **HR** · **Behavioral**
2. Choose a difficulty level: Easy / Medium / Hard
3. Click **Start Interview**

**During the interview:**
- Type your answer and press **Enter** or click **Send**
- Or hold the **🎙 microphone button** to record a voice answer — release to transcribe automatically
- The AI interviewer streams its response in real time
- The session is saved to disk — if the server restarts, the conversation is preserved

**Ending the interview:**
- Click **End & Get Debrief** (available after at least one exchange)
- Gemini generates a structured debrief with: Overall Performance · Strengths · Areas to Improve · Topics to Study · Score (out of 10)
- Click **↓ Download as Markdown** to save locally
- Click **← New Interview** to reset and start fresh

---

### Dashboard

Navigate to **Dashboard** in the left sidebar.

- **Achievements** — 9 milestone badges (First day, 3-day streak, Week warrior, 30-day legend, First problem, Problem solver, Course complete, Avid learner, MCQ master)
- **Summary stats** — animated count-up for: Day streak · Courses done · Problems solved · MCQs answered
- **7-day activity chart** — bar chart of daily actions; today highlighted in violet
- **Recommended for you** — problems and courses ranked by your weakest topics
- **Topic accuracy** — horizontal bars showing correct/seen ratio per topic
- **Focus areas** — topics below 60% accuracy
- **Strengths** — topics above 80% accuracy

---

### AI Tutor Sidebar

The tutor panel is visible on the right side of every page. It knows what you are currently doing — which course, which lesson, which problem, your current code, your failed tests — and tailors every response to that context.

**Two modes:**
- **Guide me (Socratic)** — the tutor responds with exactly one targeted question per message, nudging you toward the answer without giving it away. Best for deep learning.
- **Direct** — the tutor answers clearly and concisely. Best when you are stuck and need to move forward.

Toggle using the **Guide Me / Direct** buttons at the top of the sidebar.

**Show / hide:** Click **AI Tutor** in the left nav, or use **⌘\\** / **Ctrl+\\**. On mobile, use the **TUTOR / HIDE** button in the top bar.

**Rate limits:** If you hit the Gemini free-tier quota, the tutor displays a warning card instead of crashing.

---

### Search

Press **⌘K** (Mac) or **Ctrl+K** (Windows / Linux) from anywhere in the app.

- Type at least 2 characters to search across courses, coding problems, and MCQ tests simultaneously
- Results are ranked by title match first, then content match
- Navigate results with **↑ ↓**, select with **Enter**, or click
- Selecting a result navigates to the correct page and automatically opens that item
- Press **Esc** to close

---

### Settings

Navigate to **Settings** in the left sidebar.

**Platform Status** — shows current AI model, whether RAG is indexed, and content counts.

**Content & RAG:**
- **Re-index** — rebuilds embeddings for all course content. Run this after adding new courses.
- **Export all notes** — downloads every lesson note as a single Markdown file (`my-notes.md`).

**Tutor Preference** — set your default tutor mode.

**Data Management** — each reset requires a confirmation click:

| Action | What it clears |
|--------|----------------|
| Reset learning progress | Topic scores, completed courses & problems, activity history |
| Clear interview history | Saved interview conversation |
| Reset spaced repetition | All SM-2 review cards |
| Delete all notes | Every lesson note |
| Reset everything | All of the above at once |

---

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `⌘K` / `Ctrl+K` | Open search |
| `⌘\` / `Ctrl+\` | Toggle AI tutor sidebar |
| `?` | Open keyboard shortcuts panel |
| `Esc` | Close any open modal |
| `G` then `D` | Go to Dashboard |
| `G` then `L` | Go to Learn |
| `G` then `P` | Go to Practice |
| `G` then `I` | Go to Interview |
| `G` then `S` | Go to Settings |

> `G` shortcuts do not trigger inside text inputs or textareas.

---

## Adding Your Own Content

### Add a course

1. Create a folder in `content/courses/`. The folder name is the course ID (lowercase with hyphens, e.g. `my-course`).

2. Add `meta.json`:
```json
{
  "title": "My Course",
  "description": "A short description shown on the course card.",
  "difficulty": "beginner",
  "topics": ["arrays", "loops"]
}
```
Valid difficulty values: `beginner`, `intermediate`, `advanced`.

3. Add lesson files as Markdown (`.md`) and quiz files as JSON (`.json`, excluding `meta.json`). Files are served in alphabetical order — use a numeric prefix to control order:
```
01-introduction.md
02-arrays-in-depth.md
03-quiz.json
```

**Quiz JSON format:**
```json
{
  "questions": [
    {
      "id": "unique-id-001",
      "topic": "arrays",
      "question": "What is the time complexity of array access by index?",
      "options": ["O(1)", "O(log n)", "O(n)", "O(n²)"],
      "answer": "O(1)",
      "explanation": "Arrays store elements contiguously — the address is computed directly from the index.",
      "incorrect_explanations": {
        "O(log n)": "That is binary search, not random access.",
        "O(n)": "That would require scanning the whole array.",
        "O(n²)": "No array operation is this slow."
      }
    }
  ]
}
```

4. After adding content, go to **Settings → Re-index** so the AI tutor picks it up.

---

### Add a standalone MCQ test bank

Create a JSON file in `content/mcq/` (e.g. `content/mcq/my-topic.json`):

```json
{
  "id": "my-topic",
  "title": "My Topic Quiz",
  "topic": "my-topic",
  "questions": [
    {
      "id": "mt-001",
      "topic": "my-topic",
      "question": "Question text here?",
      "options": ["A", "B", "C", "D"],
      "answer": "A",
      "explanation": "Because..."
    }
  ]
}
```

---

### Add a coding problem

Append an entry to `content/problems/problems.json`:

```json
{
  "id": "two-sum",
  "title": "Two Sum",
  "difficulty": "easy",
  "topics": ["arrays", "hashing"],
  "description": "Given an array of integers `nums` and an integer `target`, return indices of the two numbers that add up to `target`.\n\n**Example:**\n\nInput: `nums = [2,7,11,15], target = 9`\nOutput: `[0,1]`",
  "starter_code": "def two_sum(nums, target):\n    # Write your solution here\n    pass\n",
  "test_cases": [
    { "id": 1, "input": "2 7 11 15\n9",  "expected": "[0, 1]" },
    { "id": 2, "input": "3 2 4\n6",      "expected": "[1, 2]" },
    { "id": 3, "input": "3 3\n6",        "expected": "[0, 1]" }
  ]
}
```

Valid difficulty values: `easy`, `medium`, `hard`.

**Test case format:** `input` is fed to your solution via stdin. Your script should read from `sys.stdin` and print the result. `expected` must exactly match the printed output (stripped of whitespace).

---

## API Reference

Interactive documentation is available at **`http://localhost:8000/docs`** while the backend is running.

| Method | Route | Description |
|--------|-------|-------------|
| `POST` | `/tutor/message` | Streaming SSE tutor response |
| `GET`  | `/courses` | List all courses with module counts |
| `GET`  | `/courses/{id}` | Full course content |
| `POST` | `/courses/{id}/progress` | Mark a module complete |
| `GET`  | `/practice/problems` | List coding problems |
| `GET`  | `/practice/problems/{id}` | Single problem with test cases |
| `POST` | `/practice/submit` | Run code in sandbox |
| `GET`  | `/practice/mcq` | List MCQ test banks |
| `GET`  | `/practice/mcq/review` | SM-2 review queue for today |
| `POST` | `/practice/mcq/result` | Record answer, update SR card |
| `POST` | `/interview/message` | Streaming interview turn |
| `POST` | `/interview/transcribe` | Audio blob → transcript |
| `POST` | `/interview/debrief` | Generate structured debrief |
| `POST` | `/interview/reset` | Clear interview session |
| `GET`  | `/progress/stats` | Streak, 7-day chart, topic summary |
| `GET`  | `/progress/recommendations` | Personalised problems + courses |
| `GET`  | `/notes/{course}/{module}` | Get a lesson note |
| `POST` | `/notes/{course}/{module}` | Save a lesson note |
| `GET`  | `/notes/export` | All notes as Markdown |
| `GET`  | `/search?q=...` | Search all content |
| `GET`  | `/settings/status` | Platform status |
| `POST` | `/settings/reindex` | Trigger RAG re-indexing |
| `POST` | `/settings/reset/{type}` | Reset data (`progress` / `interview` / `spaced-repetition` / `notes` / `all`) |

---

## How the AI Tutor Works

Every tutor request assembles a **three-part context package** before calling Gemini:

```
1. Current task     — page, course, lesson, problem title + description,
                      user's current code, failed test cases, active MCQ question

2. Learner profile  — topic accuracy scores from progress.json,
                      weak topics (< 60%), strong topics (≥ 80%),
                      completed courses and problems

3. RAG chunks       — top 4 relevant passages retrieved from Chroma
                      (built from your course markdown files)
```

**Socratic mode** instructs the model to respond with exactly one question per turn, chosen to move the learner one step closer to the answer.

**Direct mode** instructs the model to answer clearly and concisely, still using the full context so the answer references the learner's specific code or problem.

The interview endpoint uses a separate history list (persisted to `data/interview_history.json`) and a different system prompt — it does not share the tutor's RAG pipeline.

---

## Troubleshooting

**Backend won't start — "ModuleNotFoundError"**
Make sure your virtual environment is activated and you ran `pip install -r backend/requirements.txt`.

**"GOOGLE_API_KEY not found" error**
Check that `.env` exists in the **project root** (not inside `backend/`) and contains `GOOGLE_API_KEY=...` with no extra spaces or quotes around the value.

**429 / RESOURCE_EXHAUSTED in the tutor chat**
You have hit the Gemini free-tier rate limit. Wait a minute and try again. The tutor displays a warning card rather than crashing. Heavy use (indexing + many queries) can exhaust the daily quota — consider upgrading your API plan.

**Tutor gives generic answers and ignores course content**
The RAG index has not been built yet. Go to **Settings → Re-index**. After indexing completes, the tutor will reference specific course material.

**Code submissions always time out**
The sandbox kills processes after 5 seconds. Check for infinite loops. If your algorithm is intentionally slow, optimise it — that is the point of the problem.

**Audio transcription fails**
Microphone access must be granted in the browser. Check the browser console for specific errors and confirm your API key is valid with remaining quota.

**Frontend shows a blank page or "Network Error"**
Make sure the backend is running on port 8000 before opening the frontend. The Vite dev server proxies all `/api` calls to `http://localhost:8000` — both servers must be running.

**"Course not found" after adding new content**
Verify the folder contains a `meta.json` file. The courses endpoint only lists folders that have `meta.json`. Also run **Settings → Re-index** so the tutor picks up the new content.

**Fresh clone — backend errors on first request**
The `data/` directory is included in the repo via `data/.gitkeep`, so it will exist after cloning. All JSON data files are created automatically by the backend on first use. If you see a write error, check that you have write permissions in the project directory.

---

## License

Apache 2.0 — see [LICENSE](LICENSE).
