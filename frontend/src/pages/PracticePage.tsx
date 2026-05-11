import { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
import { fetchJSON } from "../api";
import { useStore } from "../store";
import MCQQuiz from "../components/MCQQuiz";
import CodeEditor from "../components/CodeEditor";

// ── Types ────────────────────────────────────────────────────────────────────

interface Problem {
  id: string;
  title: string;
  difficulty: string;
  topics: string[];
  description: string;
  starter_code: string;
  test_cases: { id: number; input: string; expected: string }[];
}

interface MCQTest {
  id: string;
  title: string;
  topic: string;
  count: number;
}

interface MCQTestFull {
  id: string;
  title: string;
  topic: string;
  questions: Question[];
}

interface Question {
  id: string;
  topic: string;
  question: string;
  options: string[];
  answer: string;
  explanation: string;
  incorrect_explanations?: Record<string, string>;
  source_test?: string;
}

interface ReviewQueue {
  questions: Question[];
  total_due: number;
}

const DIFFICULTY_COLOR: Record<string, string> = {
  easy:   "text-emerald-400",
  medium: "text-yellow-400",
  hard:   "text-red-400",
};

type Tab  = "coding" | "mcq" | "review";
type View =
  | { type: "list" }
  | { type: "problem";  problem: Problem }
  | { type: "mcqtest";  test: MCQTestFull }
  | { type: "review";   queue: ReviewQueue };

// ── Component ────────────────────────────────────────────────────────────────

export default function PracticePage() {
  const [tab,      setTab]      = useState<Tab>("coding");
  const [view,     setView]     = useState<View>({ type: "list" });
  const [problems, setProblems] = useState<Problem[]>([]);
  const [mcqTests, setMcqTests] = useState<MCQTest[]>([]);
  const [dueCount, setDueCount] = useState(0);
  const [loading,  setLoading]  = useState(false);
  const setTutorContext = useStore((s) => s.setTutorContext);
  const location = useLocation();

  useEffect(() => {
    setTutorContext({ page: "practice" });
    const state = location.state as { openProblem?: string; openMcq?: string } | null;

    fetchJSON<Problem[]>("/practice/problems").then((list) => {
      setProblems(list);
      if (state?.openProblem) {
        const p = list.find((x) => x.id === state.openProblem);
        if (p) openProblem(p);
      }
    }).catch(console.error);

    fetchJSON<MCQTest[]>("/practice/mcq").then((list) => {
      setMcqTests(list);
      if (state?.openMcq) {
        const t = list.find((x) => x.id === state.openMcq);
        if (t) { setTab("mcq"); openMCQ(t); }
      }
    }).catch(console.error);

    fetchJSON<ReviewQueue>("/practice/mcq/review")
      .then((q) => setDueCount(q.total_due))
      .catch(console.error);
  }, []);

  function switchTab(t: Tab) {
    setTab(t);
    setView({ type: "list" });
    setTutorContext({ page: `practice_${t}` });
  }

  async function openProblem(p: Problem) {
    setLoading(true);
    try {
      const full = await fetchJSON<Problem>(`/practice/problems/${p.id}`);
      setView({ type: "problem", problem: full });
      setTutorContext({
        page:                "practice_coding",
        problem_id:          full.id,
        problem_title:       full.title,
        problem_description: full.description.slice(0, 500),
      });
    } finally {
      setLoading(false);
    }
  }

  async function openMCQ(test: MCQTest) {
    setLoading(true);
    try {
      const full = await fetchJSON<MCQTestFull>(`/practice/mcq/${test.id}`);
      setView({ type: "mcqtest", test: full });
      setTutorContext({ page: "practice_mcq" });
    } finally {
      setLoading(false);
    }
  }

  async function openReview() {
    setLoading(true);
    try {
      const queue = await fetchJSON<ReviewQueue>("/practice/mcq/review");
      setView({ type: "review", queue });
      setTutorContext({ page: "practice_mcq" });
    } finally {
      setLoading(false);
    }
  }

  function backToList() {
    setView({ type: "list" });
    setTutorContext({ page: `practice_${tab}` });
    // Refresh due count
    fetchJSON<ReviewQueue>("/practice/mcq/review")
      .then((q) => setDueCount(q.total_due))
      .catch(console.error);
  }

  // ── Problem detail ──────────────────────────────────────────────────────────
  if (view.type === "problem") {
    return (
      <div className="h-full">
        <CodeEditor problem={view.problem} onBack={backToList} onSolved={backToList} />
      </div>
    );
  }

  // ── MCQ test view ───────────────────────────────────────────────────────────
  if (view.type === "mcqtest") {
    return (
      <div>
        <div className="flex items-center gap-4 mb-6">
          <button onClick={backToList} className="text-violet-500/70 hover:text-violet-100 text-sm transition-colors">
            ← Practice
          </button>
          <h1 className="text-xl font-bold text-violet-50">{view.test.title}</h1>
        </div>
        <div className="max-w-2xl">
          <MCQQuiz questions={view.test.questions} topic={view.test.topic} onComplete={backToList} />
        </div>
      </div>
    );
  }

  // ── Review (spaced repetition) view ────────────────────────────────────────
  if (view.type === "review") {
    const { queue } = view;
    if (queue.questions.length === 0) {
      return (
        <div>
          <div className="flex items-center gap-4 mb-6">
            <button onClick={backToList} className="text-violet-500/70 hover:text-violet-100 text-sm transition-colors">
              ← Practice
            </button>
          </div>
          <div className="text-center py-16">
            <p className="text-4xl mb-5">✅</p>
            <p className="text-violet-200 font-medium">No questions due for review</p>
            <p className="text-violet-500/70 text-sm mt-1">Come back tomorrow to keep your streak going.</p>
          </div>
        </div>
      );
    }
    return (
      <div>
        <div className="flex items-center gap-4 mb-2">
          <button onClick={backToList} className="text-violet-500/70 hover:text-violet-100 text-sm transition-colors">
            ← Practice
          </button>
          <h1 className="text-xl font-bold text-violet-50">Review Session</h1>
          <span className="text-xs text-violet-500/70 ml-auto">{queue.total_due} due today · {queue.questions.length} in session</span>
        </div>
        <div className="max-w-2xl mt-4">
          <MCQQuiz questions={queue.questions} topic="review" onComplete={backToList} />
        </div>
      </div>
    );
  }

  // ── List view ───────────────────────────────────────────────────────────────
  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold text-violet-50">Practice</h1>
        <div className="flex gap-1 glass-sm p-1">
          {(["coding", "mcq", "review"] as Tab[]).map((t) => (
            <button
              key={t}
              onClick={() => switchTab(t)}
              className={`px-4 py-1.5 rounded-md text-sm font-medium capitalize transition-all relative border ${
                tab === t
                  ? "bg-violet-600 text-violet-50 border-violet-400/50 shadow-[0_0_10px_rgba(139,92,246,0.4)]"
                  : "text-violet-400 border-transparent hover:text-violet-100 hover:bg-violet-400/10"
              }`}
            >
              {t === "coding" ? "Coding" : t === "mcq" ? "MCQ Tests" : "Review"}
              {t === "review" && dueCount > 0 && (
                <span className="absolute -top-1 -right-1 w-4 h-4 bg-red-500 text-white text-xs rounded-full flex items-center justify-center leading-none">
                  {dueCount > 9 ? "9+" : dueCount}
                </span>
              )}
            </button>
          ))}
        </div>
      </div>

      {loading && <p className="text-violet-500/70 text-sm mb-5">Loading…</p>}

      {/* Coding problems table */}
      {tab === "coding" && (
        problems.length === 0 ? (
          <p className="text-violet-500/70">No problems found. Add content to <code className="text-violet-300">content/problems/</code>.</p>
        ) : (
          <table className="w-full text-sm">
            <thead>
              <tr className="text-left text-violet-500/70 border-b border-violet-400/20">
                <th className="pb-3 font-medium">#</th>
                <th className="pb-3 font-medium">Title</th>
                <th className="pb-3 font-medium">Difficulty</th>
                <th className="pb-3 font-medium">Topics</th>
              </tr>
            </thead>
            <tbody>
              {problems.map((p, i) => (
                <tr
                  key={p.id}
                  onClick={() => openProblem(p)}
                  className="border-b border-violet-400/10 hover:bg-violet-400/8 cursor-pointer transition-all duration-150 group"
                >
                  <td className="py-3 text-violet-500/70 w-10">{i + 1}</td>
                  <td className="py-3 text-violet-100 font-medium group-hover:text-violet-100 transition-colors">{p.title}</td>
                  <td className={`py-3 font-medium capitalize ${DIFFICULTY_COLOR[p.difficulty] ?? "text-violet-400"}`}>
                    {p.difficulty}
                  </td>
                  <td className="py-3">
                    <div className="flex flex-wrap gap-1">
                      {p.topics.map((t) => (
                        <span key={t} className="text-xs bg-violet-400/10 text-violet-200 border border-violet-400/20 px-2 py-0.5 rounded">{t}</span>
                      ))}
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )
      )}

      {/* MCQ test grid */}
      {tab === "mcq" && (
        mcqTests.length === 0 ? (
          <p className="text-violet-500/70">No MCQ tests found. Add content to <code className="text-violet-300">content/mcq/</code>.</p>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {mcqTests.map((t) => (
              <button
                key={t.id}
                onClick={() => openMCQ(t)}
                className="text-left glass card-hover p-6"
              >
                <h2 className="text-base font-semibold text-violet-50 mb-1">{t.title}</h2>
                <p className="text-sm text-violet-400">{t.count} questions</p>
                <span className="mt-3 inline-block text-xs bg-violet-400/10 text-violet-200 border border-violet-400/20 px-2 py-0.5 rounded capitalize">
                  {t.topic}
                </span>
              </button>
            ))}
          </div>
        )
      )}

      {/* Review tab */}
      {tab === "review" && (
        <div className="max-w-md">
          <div className="glass card-hover p-6 text-center space-y-4">
            <div className="text-5xl">{dueCount > 0 ? "🔔" : "✅"}</div>
            <div>
              <p className="text-xl font-bold text-violet-50">
                {dueCount > 0 ? `${dueCount} questions due` : "All caught up!"}
              </p>
              <p className="text-sm text-violet-500/70 mt-1">
                {dueCount > 0
                  ? "Spaced repetition review — answer questions you've seen before."
                  : "No questions due today. Check back tomorrow."}
              </p>
            </div>
            {dueCount > 0 && (
              <button
                onClick={openReview}
                className="w-full py-2.5 bg-violet-500 hover:bg-violet-700 rounded-lg text-sm font-medium transition-colors"
              >
                Start Review Session
              </button>
            )}
          </div>
          <p className="text-xs text-violet-600/70 mt-4 text-center">
            Questions you answer in MCQ Tests are automatically scheduled for review using SM-2 spaced repetition.
          </p>
        </div>
      )}
    </div>
  );
}
