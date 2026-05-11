# Ed-AI — Vision & Plan

> **Status:** Active Draft  
> **Date:** 2026-05-11

---

## What We're Building

An AI-powered technical education platform for a single learner. The core idea: instead of giving answers, the AI tutors through the Socratic method — asking targeted questions that lead the learner to discover the answer themselves.

Three learning modes:

| Mode | What it does |
|---|---|
| **Learn** | Structured courses: markdown content + MCQ checkpoints |
| **Practice** | MCQ tests and coding problems with a live code editor |
| **Mock Interview** | Audio-driven technical and HR interview simulations |

The **Socratic AI Tutor** runs as a sidebar on every page. It always knows what the user is doing and who they are.

---

## The AI Pipeline (Core of the Product)

This is the one thing we must get right. Every other feature is secondary.

### What the tutor knows on every message

Before generating any response the backend assembles a **context package** from three sources:

```
1. CURRENT TASK — what the user is doing right now
   • Page: Learn | Practice MCQ | Practice Coding | Interview
   • If Learn:   course name, current topic/module
   • If MCQ:     question text and options
   • If Coding:  problem title, description, user's current code, failed tests
   • If Interview: type (TR/HR), turn number

2. LEARNER PROFILE — read from data/progress.json
   • Topics seen and accuracy per topic
   • Completed courses and problems
   • Known weak areas (accuracy < 60%)

3. RETRIEVED KNOWLEDGE — RAG over course content (Chroma)
   • Top 4 most relevant chunks from the course material
   • Scoped to the current course if on Learn page
```

### Socratic vs Direct mode

A toggle is visible on every page. State persists across the whole session.

| Toggle | Behaviour |
|---|---|
| **Guide me** (default) | Tutor responds only with a targeted question. Never gives the answer directly. |
| **Just tell me** | Tutor answers directly but still uses all three context sources to personalise the answer. |

### Tutor decision flow (Socratic mode)

```
Message received
      │
      ▼
Assemble context package (task + profile + RAG)
      │
      ▼
Direct answer request?
  YES → "What have you tried so far?"
  NO  → Identify the specific gap using the learner profile
      │
      ▼
Select question type:
  Clarifying  — "What does this function return?"
  Consequence — "What happens if the list is empty?"
  Analogical  — "How is this like binary search?"
      │
      ▼
Stream response (SSE)
      │
      ▼
Update progress.json with topic tag + outcome
```

---

## Tech Stack

| Layer | Choice |
|---|---|
| Frontend | React 18 + TypeScript + Vite + Tailwind CSS |
| State | Zustand (socratic toggle + session) |
| Backend | FastAPI (Python 3.11+) |
| AI | Google Gemini 1.5 Flash (tutor/interview) · 1.5 Pro (recommendations) |
| RAG | LangChain + Chroma + Google embedding-001 |
| Code execution | `subprocess` with 5s timeout |
| Storage | Plain JSON files in `data/` (single user — no DB needed) |
| Streaming | Server-Sent Events (SSE) from FastAPI to React |

No auth. No Docker. No Redis. No external judge API. No database overhead. One user.

---

## Folder Structure

```
Ed-AI/
├── backend/
│   ├── app/
│   │   ├── main.py            # FastAPI app + CORS
│   │   ├── config.py          # Pydantic settings (.env)
│   │   ├── routes/
│   │   │   ├── tutor.py       # POST /tutor/message  (SSE stream)
│   │   │   ├── courses.py     # GET  /courses, /courses/{id}
│   │   │   ├── practice.py    # GET  /problems, POST /submit
│   │   │   └── interview.py   # POST /interview/message
│   │   └── services/
│   │       ├── tutor.py       # context assembly + Gemini streaming
│   │       ├── rag.py         # Chroma vector store + retrieval
│   │       └── executor.py    # subprocess code runner
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   │   ├── LearnPage.tsx
│   │   │   ├── PracticePage.tsx
│   │   │   ├── InterviewPage.tsx
│   │   │   └── DashboardPage.tsx
│   │   ├── components/
│   │   │   ├── TutorSidebar/   # Socratic tutor + toggle
│   │   │   ├── CodeEditor/     # Monaco editor
│   │   │   └── MCQQuiz/
│   │   ├── store.ts            # Zustand
│   │   ├── api.ts              # fetch + SSE helpers
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── index.html
│   ├── package.json
│   └── vite.config.ts
│
├── content/
│   ├── courses/               # one folder per course (markdown + MCQ JSON)
│   └── problems/              # coding problem definitions (JSON)
│
├── data/
│   └── progress.json          # single-user state (topics, completions)
│
├── docs/
│   └── vision/
│       └── VISION.md
│
├── _legacy/                   # original Streamlit prototype (reference only)
├── .env
├── .gitignore
└── README.md
```

---

## Roadmap

### Phase 1 — Prototype (Now)
Get every feature working end-to-end for one user. AI pipeline is the priority.

- [ ] Backend scaffold: FastAPI, config, routes
- [ ] AI pipeline: full context package → Gemini streaming SSE ← this first
- [ ] RAG: Chroma over course content, scoped per course
- [ ] Code execution: subprocess with timeout, test case comparison
- [ ] Frontend scaffold: React + Vite + Tailwind + Zustand
- [ ] Tutor sidebar with Socratic toggle, SSE streaming display
- [ ] Learn page: course browse + markdown render + MCQ flow
- [ ] Practice page: MCQ quiz + coding editor (Monaco) + submission
- [ ] Interview page: audio capture + Gemini + TTS playback
- [ ] progress.json: write on every MCQ answer, submission, tutor outcome

### Phase 2 — Polish
Make it feel like a real product.

- [ ] Dashboard: streak, accuracy by topic, weak area highlights
- [ ] Adaptive recommendations driven by progress.json weak areas
- [ ] Full-text search across courses and problems
- [ ] Post-interview debrief (Gemini summary of the session)
- [ ] Spaced repetition for MCQs
- [ ] Concept dependency graph (unlock topics after prerequisites)

### Phase 3 — Scale (if needed)
Add multi-user support when the prototype is validated.

- [ ] Auth (JWT + Google OAuth)
- [ ] MongoDB (replace JSON files with per-user documents)
- [ ] Redis (rate limiting, JWT blocklist)
- [ ] Judge0 (replace subprocess)
- [ ] Docker Compose

---

## Open Questions

**Q1. Socratic strictness** — How many times can a user ask the same question before the tutor gives a direct hint? Suggestion: after 3 consecutive rephrases of the same question, give a partial answer.

**Q2. Content pipeline** — Who writes the course markdown? Options: hand-written, AI-generated + reviewed, imported from existing open content.

**Q3. Audio interview** — Keep push-to-record (current) or switch to continuous streaming ASR (more realistic, more complex)?
