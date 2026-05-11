import { useEffect, useRef, useState } from "react";
import Editor from "@monaco-editor/react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { postJSON } from "../../api";
import { useStore } from "../../store";
import { playSound } from "../../sounds";

interface TestCase {
  id: number;
  input: string;
  expected: string;
}

interface TestResult {
  test_id: number;
  passed: boolean;
  expected: string;
  got: string | null;
  error: string | null;
}

interface Problem {
  id: string;
  title: string;
  difficulty: string;
  topics: string[];
  description: string;
  starter_code: string;
  test_cases: TestCase[];
}

interface SubmitResponse {
  passed: number;
  total: number;
  results: TestResult[];
  status: "accepted" | "partial" | "wrong";
}

interface Props {
  problem: Problem;
  onBack: () => void;
  onSolved: () => void;
}

const DIFFICULTY_COLOR: Record<string, string> = {
  easy:   "text-emerald-400",
  medium: "text-yellow-400",
  hard:   "text-red-400",
};

export default function CodeEditor({ problem, onBack, onSolved }: Props) {
  const [code,       setCode]       = useState(problem.starter_code);
  const [results,    setResults]    = useState<SubmitResponse | null>(null);
  const [running,    setRunning]    = useState(false);
  const [solved,     setSolved]     = useState(false);
  const { setTutorContext } = useStore();
  const debounceRef = useRef<ReturnType<typeof setTimeout>>();

  // Update tutor context whenever code changes
  useEffect(() => {
    clearTimeout(debounceRef.current);
    debounceRef.current = setTimeout(() => {
      setTutorContext({
        page:                "practice_coding",
        problem_id:          problem.id,
        problem_title:       problem.title,
        problem_description: problem.description.slice(0, 500),
        user_code:           code,
        failed_tests:        results?.results.filter((r) => !r.passed) ?? undefined,
      });
    }, 800);
  }, [code, results]);

  async function runCode() {
    setRunning(true);
    playSound("run");
    try {
      const res = await postJSON<SubmitResponse>("/practice/submit", {
        problem_id:  problem.id,
        source_code: code,
      });
      setResults(res);
      if (res.status === "accepted") {
        playSound("pass");
        setSolved(true);
        onSolved();
      } else {
        playSound("fail");
      }
    } catch (e) {
      console.error(e);
    } finally {
      setRunning(false);
    }
  }

  return (
    <div className="flex h-full gap-0 overflow-hidden rounded-lg border border-violet-400/20">
      {/* Left: problem description */}
      <div className="w-2/5 flex flex-col border-r border-violet-400/15 overflow-hidden">
        <div className="px-4 py-3 border-b border-violet-400/15 flex items-center gap-3 bg-[#111128]">
          <button onClick={onBack} className="text-violet-500/70 hover:text-violet-100 text-sm transition-colors">
            ← Back
          </button>
          <span className={`text-xs font-medium capitalize ${DIFFICULTY_COLOR[problem.difficulty] ?? "text-violet-400"}`}>
            {problem.difficulty}
          </span>
        </div>

        <div className="flex-1 overflow-y-auto p-5 prose-rpg">
          <h1 className="text-lg font-bold text-violet-50 mb-3">{problem.title}</h1>
          <div className="flex flex-wrap gap-1 mb-4">
            {problem.topics.map((t) => (
              <span key={t} className="text-xs bg-violet-400/10 text-violet-200 border border-violet-400/20 px-2 py-0.5 rounded">{t}</span>
            ))}
          </div>
          <ReactMarkdown remarkPlugins={[remarkGfm]}>
            {problem.description}
          </ReactMarkdown>
        </div>
      </div>

      {/* Right: editor + results */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Toolbar */}
        <div className="px-4 py-2 border-b border-violet-400/15 flex items-center justify-between bg-[#111128]">
          <span className="text-xs text-violet-500/70 font-mono">Python 3</span>
          <button
            onClick={runCode}
            disabled={running || solved}
            className={`px-4 py-1.5 rounded-lg text-sm font-medium transition-all ${
              solved
                ? "bg-emerald-700 text-white cursor-default shadow-[0_0_10px_rgba(52,211,153,0.3)]"
                : "bg-violet-500 hover:bg-violet-400 disabled:opacity-50 shadow-[0_0_10px_rgba(139,92,246,0.4)]"
            }`}
          >
            {solved ? "✓ Solved" : running ? "Running…" : "Run Code"}
          </button>
        </div>

        {/* Monaco editor */}
        <div className={`flex-1 overflow-hidden ${running ? "running-border" : ""}`}>
          <Editor
            height="100%"
            defaultLanguage="python"
            value={code}
            theme="vs-dark"
            onChange={(v) => setCode(v ?? "")}
            options={{
              fontSize: 14,
              minimap:  { enabled: false },
              padding:  { top: 12 },
              scrollBeyondLastLine: false,
            }}
          />
        </div>

        {/* Test results */}
        {results && (
          <div className="border-t border-violet-400/15 max-h-48 overflow-y-auto p-4 space-y-3 bg-[#080318]">
            <div className="flex items-center gap-3 mb-2">
              <span className={`text-sm font-semibold ${
                results.status === "accepted" ? "text-emerald-400" :
                results.status === "partial"  ? "text-yellow-400" : "text-red-400"
              }`}>
                {results.passed}/{results.total} tests passed
              </span>
            </div>
            {results.results.map((r, i) => {
              const stagger = ["d-50","d-100","d-150","d-200","d-250","d-300"];
              return (
              <div key={r.test_id}
                className={`card-enter ${stagger[i] ?? ""} rounded p-2 text-xs font-mono ${r.passed ? "bg-emerald-900/20 text-emerald-300" : "bg-red-900/20 text-red-300"}`}>
                <span className="font-bold">Test {r.test_id}</span>
                {r.error
                  ? <> · <span className="text-red-400">{r.error}</span></>
                  : r.passed
                    ? <> · <span>✓ Passed</span></>
                    : <> · Expected <code>{r.expected}</code>, got <code>{r.got ?? "null"}</code></>
                }
              </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
}
