import { useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import { fetchJSON } from "../../api";

interface SearchResult {
  type: "course" | "problem" | "mcq";
  id: string; title: string; snippet: string; difficulty?: string; score: number;
}

interface Props { onClose: () => void; }

const TYPE_LABEL: Record<string, string> = { course: "Course", problem: "Problem", mcq: "MCQ Test" };
const TYPE_COLOR: Record<string, string> = {
  course:  "bg-violet-400/20 text-violet-200 border border-violet-400/30",
  problem: "bg-blue-500/20 text-blue-300 border border-blue-500/30",
  mcq:     "bg-violet-500/20 text-violet-300 border border-violet-500/30",
};

export default function SearchModal({ onClose }: Props) {
  const [query,   setQuery]   = useState("");
  const [results, setResults] = useState<SearchResult[]>([]);
  const [active,  setActive]  = useState(0);
  const inputRef = useRef<HTMLInputElement>(null);
  const navigate = useNavigate();

  useEffect(() => { inputRef.current?.focus(); }, []);

  useEffect(() => {
    if (query.length < 2) { setResults([]); return; }
    const t = setTimeout(() => {
      fetchJSON<{ results: SearchResult[] }>(`/search?q=${encodeURIComponent(query)}`)
        .then((d) => { setResults(d.results); setActive(0); })
        .catch(() => {});
    }, 250);
    return () => clearTimeout(t);
  }, [query]);

  function go(r: SearchResult) {
    onClose();
    if (r.type === "course")  navigate("/",         { state: { openCourse:  r.id } });
    if (r.type === "problem") navigate("/practice", { state: { openProblem: r.id } });
    if (r.type === "mcq")     navigate("/practice", { state: { openMcq:     r.id } });
  }

  function onKey(e: React.KeyboardEvent) {
    if (e.key === "Escape")    { onClose(); return; }
    if (e.key === "ArrowDown") { setActive((a) => Math.min(a + 1, results.length - 1)); e.preventDefault(); }
    if (e.key === "ArrowUp")   { setActive((a) => Math.max(a - 1, 0)); e.preventDefault(); }
    if (e.key === "Enter" && results[active]) go(results[active]);
  }

  return (
    <div className="fixed inset-0 z-50 flex items-start justify-center pt-20 bg-black/80 px-4" onClick={onClose}>
      <div
        className="w-full max-w-xl bg-[#080418] overflow-hidden"
        style={{ border: "3px solid #8b5cf6", boxShadow: "5px 5px 0 #2e1065", borderRadius: 2 }}
        onClick={(e) => e.stopPropagation()}
      >
        {/* Title bar */}
        <div className="flex items-center gap-3 px-4 py-2 bg-violet-500/15 border-b-2 border-dashed border-violet-600/40">
          <span className="pixel text-[8px] text-violet-400 tracking-wider">🔍 SEARCH</span>
        </div>
        {/* Input */}
        <div className="flex items-center gap-3 px-4 py-3 border-b border-dashed border-violet-700/30">
          <input
            ref={inputRef}
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={onKey}
            placeholder="Search courses, problems, tests…"
            className="flex-1 bg-transparent text-violet-100 text-sm outline-none placeholder-violet-800"
          />
          <kbd className="pixel text-[8px] text-violet-500 bg-violet-400/10 border border-violet-500/30 px-1.5 py-0.5" style={{ borderRadius: 2 }}>ESC</kbd>
        </div>

        {/* Results */}
        {results.length > 0 && (
          <ul className="max-h-80 overflow-y-auto py-2">
            {results.map((r, i) => (
              <li key={`${r.type}-${r.id}-${i}`}>
                <button
                  onClick={() => go(r)}
                  onMouseEnter={() => setActive(i)}
                  className={`w-full text-left px-4 py-3 flex items-start gap-3 transition-colors ${
                    i === active ? "bg-violet-400/10 border-l-2 border-violet-400" : "hover:bg-violet-400/5"
                  }`}
                >
                  <span className={`text-xs px-2 py-0.5 rounded-full shrink-0 mt-0.5 ${TYPE_COLOR[r.type]}`}>
                    {TYPE_LABEL[r.type]}
                  </span>
                  <div className="min-w-0 flex-1">
                    <p className="text-sm text-violet-50 font-medium truncate">{r.title}</p>
                    <p className="text-xs text-violet-500/70 mt-0.5 line-clamp-1">{r.snippet}</p>
                  </div>
                  {r.difficulty && (
                    <span className="text-xs text-violet-600/70 shrink-0 capitalize">{r.difficulty}</span>
                  )}
                </button>
              </li>
            ))}
          </ul>
        )}

        {query.length >= 2 && results.length === 0 && (
          <p className="text-violet-600/70 text-sm text-center py-10">No results for "{query}"</p>
        )}
        {query.length < 2 && (
          <p className="text-violet-700/70 text-xs text-center py-8">Type at least 2 characters to search</p>
        )}
      </div>
    </div>
  );
}
