import { useEffect, useRef, useState } from "react";
import { useLocation } from "react-router-dom";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { fetchJSON, postJSON } from "../api";
import { useStore } from "../store";
import MCQQuiz from "../components/MCQQuiz";

interface CourseMeta {
  id: string;
  title: string;
  description: string;
  difficulty: string;
  topics: string[];
  module_count: number;
}

interface Module {
  type: "lesson" | "mcq";
  file: string;
  content: string | { questions: Question[] };
}

interface Question {
  id: string;
  topic: string;
  question: string;
  options: string[];
  answer: string;
  explanation: string;
  incorrect_explanations?: Record<string, string>;
}

interface CourseData {
  id: string;
  meta: CourseMeta;
  modules: Module[];
}

const DIFFICULTY_COLOR: Record<string, string> = {
  beginner:     "text-emerald-400",
  intermediate: "text-yellow-400",
  advanced:     "text-red-400",
};

type View =
  | { type: "browse" }
  | { type: "course"; data: CourseData; moduleIndex: number };

// ── Notes panel ─────────────────────────────────────────────────────────────

function NotesPanel({ courseId, moduleIndex }: { courseId: string; moduleIndex: number }) {
  const [text,   setText]   = useState("");
  const [saved,  setSaved]  = useState(false);
  const timerRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  useEffect(() => {
    fetchJSON<{ text: string }>(`/notes/${courseId}/${moduleIndex}`)
      .then((r) => setText(r.text))
      .catch(() => {});
  }, [courseId, moduleIndex]);

  function onChange(val: string) {
    setText(val);
    setSaved(false);
    if (timerRef.current) clearTimeout(timerRef.current);
    timerRef.current = setTimeout(() => {
      postJSON(`/notes/${courseId}/${moduleIndex}`, { text: val })
        .then(() => setSaved(true))
        .catch(() => {});
    }, 800);
  }

  return (
    <div className="mt-6 border-t border-violet-400/10 pt-4">
      <div className="flex items-center justify-between mb-2">
        <p className="text-xs text-violet-500/70 font-medium uppercase tracking-wide">Notes</p>
        {saved && <span className="text-xs text-emerald-400">Saved</span>}
      </div>
      <textarea
        value={text}
        onChange={(e) => onChange(e.target.value)}
        placeholder="Jot notes for this lesson…"
        rows={4}
        className="w-full glass-input rounded-lg px-3 py-2 text-sm text-violet-100 placeholder-violet-800 outline-none focus:ring-1 focus:ring-violet-400/50 resize-y"
      />
    </div>
  );
}

// ── Main component ────────────────────────────────────────────────────────────

export default function LearnPage() {
  const [courses,  setCourses]  = useState<CourseMeta[]>([]);
  const [progress, setProgress] = useState<Record<string, Record<string, boolean>>>({});
  const [view,     setView]     = useState<View>({ type: "browse" });
  const [loading,  setLoading]  = useState(false);
  const setTutorContext = useStore((s) => s.setTutorContext);
  const location = useLocation();

  useEffect(() => {
    setTutorContext({ page: "learn" });
    Promise.all([
      fetchJSON<CourseMeta[]>("/courses"),
      fetchJSON<{ course_progress?: Record<string, Record<string, boolean>> }>("/progress"),
    ]).then(([list, prog]) => {
      setCourses(list);
      setProgress(prog.course_progress ?? {});
      const id = (location.state as { openCourse?: string } | null)?.openCourse;
      if (id) openCourse(id);
    }).catch(console.error);
  }, []);

  async function openCourse(id: string) {
    setLoading(true);
    try {
      const data = await fetchJSON<CourseData>(`/courses/${id}`);
      setView({ type: "course", data, moduleIndex: 0 });
      setTutorContext({
        page:          "learn",
        course_id:     id,
        course_title:  data.meta.title,
        current_topic: data.meta.topics?.[0],
      });
    } finally {
      setLoading(false);
    }
  }

  function goToModule(v: Extract<View, { type: "course" }>, idx: number) {
    const mod = v.data.modules[idx];
    setView({ ...v, moduleIndex: idx });
    setTutorContext({
      page:          "learn",
      course_id:     v.data.id,
      course_title:  v.data.meta.title,
      current_topic: mod?.file ?? v.data.meta.topics?.[0],
    });
  }

  async function completeModule(v: Extract<View, { type: "course" }>) {
    await postJSON(`/courses/${v.data.id}/progress`, {
      module_index: v.moduleIndex,
      completed: true,
    }).catch(() => {});

    // Update local progress state
    setProgress((prev) => ({
      ...prev,
      [v.data.id]: { ...(prev[v.data.id] ?? {}), [String(v.moduleIndex)]: true },
    }));

    if (v.moduleIndex < v.data.modules.length - 1) {
      goToModule(v, v.moduleIndex + 1);
    } else {
      setView({ type: "browse" });
      setTutorContext({ page: "learn" });
    }
  }

  // ── Browse view ─────────────────────────────────────────────────────────────
  if (view.type === "browse") {
    return (
      <div>
        <h1 className="text-2xl font-bold text-violet-50 mb-6">Learn</h1>
        {loading && <p className="text-violet-500/70 text-sm mb-5">Loading…</p>}
        {courses.length === 0 ? (
          <p className="text-violet-500/70">
            No courses found. Add content to <code className="text-violet-300">content/courses/</code>.
          </p>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {courses.map((c, idx) => {
              const done  = Object.values(progress[c.id] ?? {}).filter(Boolean).length;
              const total = c.module_count;
              const pct   = total > 0 ? Math.round((done / total) * 100) : 0;
              const stagger = ["d-50","d-100","d-150","d-200","d-250","d-300","d-350","d-400","d-450","d-500"];
              return (
                <button
                  key={c.id}
                  onClick={() => openCourse(c.id)}
                  className={`text-left glass card-hover p-6 card-enter ${stagger[idx] ?? "d-500"}`}
                >
                  <p className={`text-xs font-medium uppercase tracking-wide mb-1 capitalize ${DIFFICULTY_COLOR[c.difficulty] ?? "text-violet-400"}`}>
                    {c.difficulty}
                  </p>
                  <h2 className="text-base font-semibold text-violet-50 mb-2">{c.title}</h2>
                  <p className="text-sm text-violet-400 mb-5 line-clamp-2">{c.description}</p>

                  {/* Progress bar */}
                  {total > 0 && (
                    <div className="mb-5">
                      <div className="flex justify-between text-xs text-violet-500/70 mb-1">
                        <span>{done}/{total} modules</span>
                        <span>{pct}%</span>
                      </div>
                      <div className="w-full h-1.5 bg-violet-400/10 rounded-full overflow-hidden">
                        <div
                          className={`h-full rounded-full transition-all ${pct === 100 ? "bg-emerald-500" : "bg-violet-500"}`}
                          style={{ width: `${pct}%` }}
                        />
                      </div>
                    </div>
                  )}

                  <div className="flex flex-wrap gap-1">
                    {c.topics?.map((t) => (
                      <span key={t} className="text-xs bg-violet-400/10 text-violet-200 border border-violet-400/20 px-2 py-0.5 rounded">{t}</span>
                    ))}
                  </div>
                </button>
              );
            })}
          </div>
        )}
      </div>
    );
  }

  // ── Course view ─────────────────────────────────────────────────────────────
  const { data, moduleIndex } = view;
  const mod      = data.modules[moduleIndex];
  const isLesson = mod?.type === "lesson";
  const isQuiz   = mod?.type === "mcq";
  const quizData = isQuiz ? (mod.content as { questions: Question[] }) : null;

  return (
    <div className="flex flex-col h-full">
      {/* Header */}
      <div className="flex items-center gap-4 mb-5">
        <button
          onClick={() => { setView({ type: "browse" }); setTutorContext({ page: "learn" }); }}
          className="text-violet-500/70 hover:text-violet-100 text-sm transition-colors"
        >
          ← All Courses
        </button>
        <div>
          <h1 className="text-xl font-bold text-violet-50">{data.meta.title}</h1>
          <p className="text-xs text-violet-500/70 mt-0.5">
            Module {moduleIndex + 1} of {data.modules.length}
          </p>
        </div>
      </div>

      {/* Module tabs */}
      <div className="flex gap-1 mb-5 flex-wrap">
        {data.modules.map((m, i) => {
          const done = progress[data.id]?.[String(i)];
          return (
            <button
              key={i}
              onClick={() => goToModule(view, i)}
              className={`px-3 py-1.5 rounded-md text-xs font-medium transition-all duration-150 flex items-center gap-1 border ${
                i === moduleIndex
                  ? "bg-violet-600 text-violet-50 border-violet-300/40 shadow-[0_0_12px_rgba(139,92,246,0.45)] scale-[1.03]"
                  : "bg-[#150830] border-violet-400/15 text-violet-400 hover:text-white hover:bg-violet-400/15 hover:border-violet-400/45 hover:shadow-[0_0_6px_rgba(139,92,246,0.15)]"
              }`}
            >
              {done && <span className="text-emerald-400">✓</span>}
              {m.type === "lesson" ? `Lesson ${i + 1}` : `Quiz ${i + 1}`}
            </button>
          );
        })}
      </div>

      {/* Module content */}
      <div className="flex-1 overflow-y-auto">
        {isLesson && (
          <>
            <div className="prose-rpg max-w-3xl px-1 pb-8">
              <ReactMarkdown remarkPlugins={[remarkGfm]}>
                {mod.content as string}
              </ReactMarkdown>
            </div>
            <NotesPanel courseId={data.id} moduleIndex={moduleIndex} />
          </>
        )}

        {isQuiz && quizData && (
          <div className="max-w-2xl">
            <MCQQuiz
              questions={quizData.questions}
              topic={data.meta.topics?.[0] ?? "general"}
              onComplete={() => completeModule(view)}
            />
          </div>
        )}
      </div>

      {/* Navigation footer (lesson only — quiz handles its own next) */}
      {isLesson && (
        <div className="pt-5 border-t border-violet-400/10 mt-5 flex justify-between">
          <button
            onClick={() => goToModule(view, moduleIndex - 1)}
            disabled={moduleIndex === 0}
            className="px-4 py-2 bg-[#150830] border border-violet-400/20 hover:border-violet-400/50 disabled:opacity-30 rounded-lg text-sm font-medium transition-all"
          >
            Previous
          </button>
          <button
            onClick={() => completeModule(view)}
            className="px-4 py-2 bg-violet-500 hover:bg-violet-400 rounded-lg text-sm font-medium transition-all shadow-[0_0_12px_rgba(139,92,246,0.4)]"
          >
            {moduleIndex < data.modules.length - 1 ? "Next Module" : "Complete Course"}
          </button>
        </div>
      )}
    </div>
  );
}
