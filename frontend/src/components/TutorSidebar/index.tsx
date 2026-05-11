import { useState, useRef, useEffect } from "react";
import { useStore } from "../../store";
import { streamTutorMessage } from "../../api";
import { playSound } from "../../sounds";

interface Message {
  role: "user" | "tutor" | "error";
  content: string;
}

interface Props {
  onClose?: () => void;
}

export default function TutorSidebar({ onClose }: Props) {
  const { socraticMode, setSocraticMode, tutorContext } = useStore();
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput]       = useState("");
  const [loading, setLoading]   = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  async function send() {
    const text = input.trim();
    if (!text || loading) return;

    setMessages((m) => [...m, { role: "user", content: text }]);
    setInput("");
    setLoading(true);
    playSound("send");
    setMessages((m) => [...m, { role: "tutor", content: "" }]);

    await streamTutorMessage(
      { message: text, socratic_mode: socraticMode, context: tutorContext },
      (token) => {
        setMessages((m) => {
          const updated = [...m];
          updated[updated.length - 1] = {
            role: "tutor",
            content: updated[updated.length - 1].content + token,
          };
          return updated;
        });
      },
      (err) => {
        const msg = err === "rate_limit"
          ? "API quota reached — try again in a moment."
          : `Error: ${err}`;
        setMessages((m) => {
          const updated = [...m];
          updated[updated.length - 1] = { role: "error", content: msg };
          return updated;
        });
      },
    );

    setLoading(false);
  }

  return (
    <aside className="w-96 shrink-0 flex flex-col border-l-4 border-violet-700/50 bg-[#08041a]">
      {/* Header */}
      <div className="px-5 py-5 border-b-2 border-dashed border-violet-700/40 flex items-center justify-between bg-[#080318]">
        <div>
          <p className="pixel text-[9px] text-violet-400 drop-shadow-[0_0_6px_rgba(139,92,246,0.6)]">🤖 AI TUTOR</p>
          <p className="text-xs text-violet-600/70 mt-2">
            {socraticMode ? "Socratic mode" : "Direct mode"}
          </p>
        </div>
        {onClose && (
          <button
            onClick={onClose}
            className="pixel text-[10px] text-violet-600/70 hover:text-violet-300 border border-violet-700/40 px-2.5 py-1.5 hover:border-violet-500/60 transition-colors"
            style={{ borderRadius: 2 }}
          >
            ✕
          </button>
        )}
      </div>

      {/* Mode toggle */}
      <div className="px-5 py-4 border-b border-dashed border-violet-700/30 flex gap-3">
        <button
          onClick={() => setSocraticMode(true)}
          className={`flex-1 py-2.5 pixel text-[7px] tracking-wider transition-all duration-100 border-2 ${
            socraticMode
              ? "bg-violet-600 text-violet-50 border-violet-300 shadow-[2px_2px_0_#2e1065]"
              : "bg-transparent border-violet-700/40 text-violet-500/70 hover:text-violet-200 hover:border-violet-500/50"
          }`}
          style={{ borderRadius: 2 }}
        >
          GUIDE ME
        </button>
        <button
          onClick={() => setSocraticMode(false)}
          className={`flex-1 py-2.5 pixel text-[7px] tracking-wider transition-all duration-100 border-2 ${
            !socraticMode
              ? "bg-violet-800 text-violet-100 border-violet-600 shadow-[2px_2px_0_#2e1065]"
              : "bg-transparent border-violet-700/40 text-violet-500/70 hover:text-violet-200 hover:border-violet-500/50"
          }`}
          style={{ borderRadius: 2 }}
        >
          DIRECT
        </button>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto px-5 py-5 space-y-4">
        {messages.length === 0 && (
          <div className="text-center mt-14 space-y-5">
            <p className="text-5xl float">🧠</p>
            <p className="pixel text-[7px] text-violet-800/70 leading-relaxed tracking-wide">ASK ANYTHING<br/>ABOUT YOUR QUEST</p>
          </div>
        )}
        {messages.map((m, i) => (
          <div
            key={i}
            className={`text-sm px-4 py-3 whitespace-pre-wrap leading-relaxed border-2 ${
              m.role === "user"
                ? "msg-right bg-violet-500/15 border-violet-500/40 text-violet-100 ml-8 shadow-[2px_2px_0_#2e1065]"
                : m.role === "error"
                ? "msg-left bg-red-900/30 border-red-600/50 text-red-300 mr-8"
                : "msg-left bg-[#150830] border-violet-700/40 text-violet-100 mr-8"
            }`}
            style={{ borderRadius: 2 }}
          >
            {m.content || <span className="animate-pulse text-violet-600">▌</span>}
          </div>
        ))}
        <div ref={bottomRef} />
      </div>

      {/* Input */}
      <div className="px-5 py-4 border-t-2 border-dashed border-violet-700/40 flex gap-3">
        <input
          className="flex-1 glass-input px-4 py-2.5 text-sm outline-none"
          style={{ borderRadius: 2 }}
          placeholder="Your message..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && !e.shiftKey && send()}
          disabled={loading}
        />
        <button
          onClick={send}
          disabled={loading || !input.trim()}
          className="rpg-btn px-4 py-2.5 disabled:opacity-40"
        >
          ▶
        </button>
      </div>
    </aside>
  );
}
