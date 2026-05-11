import { useEffect, useRef, useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { useStore } from "../store";

const BASE = "/api";

interface Message { role: "user" | "interviewer" | "error"; content: string; }

const TYPE_OPTIONS = [
  ["technical",    "Technical"],
  ["system_design","System Design"],
  ["hr",           "HR"],
  ["behavioral",   "Behavioral"],
] as const;

export default function InterviewPage() {
  const setTutorContext = useStore((s) => s.setTutorContext);
  const [type,       setType]       = useState<"technical" | "hr" | "system_design" | "behavioral">("technical");
  const [difficulty, setDiff]       = useState("medium");
  const [messages,   setMessages]   = useState<Message[]>([]);
  const [input,      setInput]      = useState("");
  const [started,    setStarted]    = useState(false);
  const [loading,    setLoading]    = useState(false);
  const [recording,  setRecording]  = useState(false);
  const [debrief,    setDebrief]    = useState<string | null>(null);
  const [debriefing, setDebriefing] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);
  const mediaRef  = useRef<MediaRecorder | null>(null);
  const chunksRef = useRef<Blob[]>([]);

  useEffect(() => { setTutorContext({ page: "interview" }); }, []);
  useEffect(() => { bottomRef.current?.scrollIntoView({ behavior: "smooth" }); }, [messages]);

  async function start() {
    await fetch(`${BASE}/interview/reset`, { method: "POST" });
    setMessages([]); setDebrief(null); setStarted(true);
    await send("Hello, I'm ready to start the interview.");
  }

  async function endInterview() {
    setDebriefing(true);
    try {
      const res  = await fetch(`${BASE}/interview/debrief`, { method: "POST" });
      const data = await res.json();
      setDebrief(data.debrief ?? "No debrief available.");
    } catch { setDebrief("Failed to generate debrief."); }
    finally  { setDebriefing(false); }
  }

  async function send(text?: string) {
    const msg = (text ?? input).trim();
    if (!msg || loading) return;
    setInput("");
    setMessages((m) => [...m, { role: "user", content: msg }]);
    setLoading(true);
    setMessages((m) => [...m, { role: "interviewer", content: "" }]);

    const res     = await fetch(`${BASE}/interview/message`, {
      method: "POST", headers: { "Content-Type": "application/json" },
      body:   JSON.stringify({ message: msg, interview_type: type, difficulty }),
    });
    const reader  = res.body!.getReader();
    const decoder = new TextDecoder();
    outer: while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      for (const line of decoder.decode(value).split("\n")) {
        if (!line.startsWith("data: ")) continue;
        const d = line.slice(6);
        if (d === "[DONE]") break outer;
        try {
          const { token } = JSON.parse(d);
          if (!token) continue;
          if (token.startsWith("\x00")) {
            const errMsg = token === "\x00RATE_LIMIT" ? "API quota reached — try again." : `Error: ${token.slice(7)}`;
            setMessages((m) => { const u = [...m]; u[u.length-1] = { role: "error", content: errMsg }; return u; });
            break outer;
          }
          setMessages((m) => { const u = [...m]; u[u.length-1] = { role: "interviewer", content: u[u.length-1].content + token }; return u; });
        } catch { /**/ }
      }
    }
    setLoading(false);
  }

  async function startRecording() {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mr = new MediaRecorder(stream);
      chunksRef.current = [];
      mr.ondataavailable = (e) => { if (e.data.size > 0) chunksRef.current.push(e.data); };
      mr.start(); mediaRef.current = mr; setRecording(true);
    } catch { alert("Microphone access denied."); }
  }

  async function stopRecording() {
    const mr = mediaRef.current;
    if (!mr) return;
    setRecording(false); setLoading(true);
    await new Promise<void>((resolve) => { mr.onstop = () => resolve(); mr.stop(); mr.stream.getTracks().forEach((t) => t.stop()); });
    const blob   = new Blob(chunksRef.current, { type: "audio/webm" });
    const reader = new FileReader();
    reader.readAsDataURL(blob);
    reader.onloadend = async () => {
      const b64 = (reader.result as string).split(",")[1];
      try {
        const res = await fetch(`${BASE}/interview/transcribe`, {
          method: "POST", headers: { "Content-Type": "application/json" },
          body:   JSON.stringify({ audio_b64: b64, mime_type: "audio/webm" }),
        });
        const { text } = await res.json();
        if (text && !text.startsWith("[")) setInput(text);
      } catch { /**/ }
      setLoading(false);
    };
  }

  // ── Debrief view ──────────────────────────────────────────────────────────
  if (debrief !== null) {
    return (
      <div className="max-w-2xl space-y-5">
        <div className="flex items-center gap-4">
          <button onClick={() => { setStarted(false); setDebrief(null); setMessages([]); }}
            className="text-violet-500/70 hover:text-violet-100 text-sm transition-colors">
            ← New Interview
          </button>
          <h1 className="text-xl font-bold text-violet-50">Interview Debrief</h1>
        </div>
        {debriefing ? (
          <p className="text-violet-500/70 text-sm animate-pulse">Generating debrief…</p>
        ) : (
          <>
            <div className="glass p-6 prose-rpg">
              <ReactMarkdown remarkPlugins={[remarkGfm]}>{debrief}</ReactMarkdown>
            </div>
            <button
              onClick={() => {
                const url = URL.createObjectURL(new Blob([debrief ?? ""], { type: "text/markdown" }));
                const a   = Object.assign(document.createElement("a"), { href: url, download: `interview-debrief-${new Date().toISOString().slice(0,10)}.md` });
                a.click(); URL.revokeObjectURL(url);
              }}
              className="text-xs text-violet-500/70 hover:text-violet-200 transition-colors"
            >
              ↓ Download as Markdown
            </button>
          </>
        )}
      </div>
    );
  }

  // ── Setup view ────────────────────────────────────────────────────────────
  if (!started) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh]">
        <div className="w-full max-w-md space-y-6">
          <div className="text-center">
            <h1 className="text-3xl font-bold text-violet-50 mb-2">Mock Interview</h1>
            <p className="text-sm text-violet-500/70">Choose your interview type and difficulty to begin.</p>
          </div>

          <div className="glass p-6 space-y-5">
            <div>
              <p className="text-xs font-semibold text-violet-500/70 uppercase tracking-widest mb-5">Interview type</p>
              <div className="grid grid-cols-2 gap-3">
                {TYPE_OPTIONS.map(([val, label]) => (
                  <button key={val} onClick={() => setType(val)}
                    className={`py-2.5 rounded-xl text-sm font-medium transition-all ${
                      type === val
                        ? "bg-violet-600 text-violet-50 border border-violet-400/50 shadow-[0_0_12px_rgba(139,92,246,0.45)]"
                        : "bg-[#150830] border border-violet-400/20 text-violet-400 hover:text-violet-100 hover:border-violet-400/50"
                    }`}>
                    {label}
                  </button>
                ))}
              </div>
            </div>

            <div>
              <p className="text-xs font-semibold text-violet-500/70 uppercase tracking-widest mb-5">Difficulty</p>
              <select value={difficulty} onChange={(e) => setDiff(e.target.value)}
                className="w-full glass-input rounded-xl px-4 py-3 text-sm text-violet-100 outline-none focus:ring-1 focus:ring-violet-400/50 appearance-none cursor-pointer">
                <option value="easy">Easy</option>
                <option value="medium">Medium</option>
                <option value="hard">Hard</option>
              </select>
            </div>

            <button onClick={start}
              className="w-full py-3 bg-violet-500 hover:bg-violet-400 rounded-lg text-sm font-semibold transition-all shadow-[0_0_14px_rgba(139,92,246,0.5)]">
              Start Interview
            </button>
          </div>
        </div>
      </div>
    );
  }

  // ── Chat view ─────────────────────────────────────────────────────────────
  return (
    <div className="flex flex-col h-full max-h-[calc(100vh-6rem)]">
      <div className="flex items-center justify-between mb-5">
        <h1 className="text-2xl font-bold text-violet-50">Mock Interview</h1>
        <button
          onClick={endInterview}
          disabled={debriefing || messages.length < 2}
          className="px-4 py-2 bg-[#150830] hover:bg-violet-400/10 border border-violet-400/20 hover:border-violet-400/50 disabled:opacity-30 rounded-lg text-sm font-medium transition-all"
        >
          End & Get Debrief
        </button>
      </div>

      <div className="flex flex-col flex-1 overflow-hidden glass">
        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-5 space-y-3">
          {messages.map((m, i) => (
            <div key={i} className={`text-sm rounded-lg px-4 py-3 max-w-[85%] whitespace-pre-wrap leading-relaxed border ${
              m.role === "user"
                ? "bg-violet-500/20 border-violet-400/30 ml-auto text-violet-50"
                : m.role === "error"
                ? "bg-violet-500/10 border-violet-500/30 text-violet-300"
                : "bg-[#150830] border-violet-400/15 text-violet-100"
            }`}>
              {m.content || <span className="animate-pulse text-violet-500/70">▌</span>}
            </div>
          ))}
          <div ref={bottomRef} />
        </div>

        {/* Input bar */}
        <div className="p-5 border-t border-violet-400/10 flex gap-3 items-center">
          <input
            className="flex-1 glass-input rounded-lg px-4 py-3 text-sm text-violet-50 placeholder-violet-700 outline-none focus:ring-1 focus:ring-violet-400/50"
            placeholder={recording ? "Recording… release to transcribe" : "Your answer…"}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && !e.shiftKey && send()}
            disabled={loading || recording}
          />
          <button
            onMouseDown={startRecording} onMouseUp={stopRecording}
            onTouchStart={startRecording} onTouchEnd={stopRecording}
            disabled={loading} title="Hold to record"
            className={`p-2.5 rounded-xl text-sm transition-all disabled:opacity-40 ${
              recording
                ? "bg-red-500 text-white animate-pulse shadow-[0_0_12px_rgba(239,68,68,0.5)]"
                : "bg-[#150830] border border-violet-400/20 hover:border-violet-400/50 text-violet-200"
            }`}
          >
            🎙
          </button>
          <button
            onClick={() => send()}
            disabled={loading || !input.trim() || recording}
            className="px-4 py-2.5 bg-violet-500 hover:bg-violet-400 disabled:opacity-40 rounded-lg text-sm font-medium transition-all shadow-[0_0_10px_rgba(139,92,246,0.4)]"
          >
            Send
          </button>
        </div>
      </div>
    </div>
  );
}
