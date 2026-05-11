import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

const STORAGE_KEY = "edai_onboarded";

const STEPS = [
  { icon: "📚", title: "Learn from structured courses",   body: "Work through lessons and quizzes on DSA, algorithms, and programming. Progress bars track your completion." },
  { icon: "💻", title: "Practice with real problems",     body: "Solve coding problems in a Monaco editor with a sandboxed Python runner. MCQ tests with spaced-repetition keep concepts sharp." },
  { icon: "🎤", title: "Mock interviews with AI",         body: "Pick Technical, System Design, HR, or Behavioral. Practice with streaming AI responses and get a scored debrief at the end." },
  { icon: "🤖", title: "AI Tutor always at your side",   body: 'The tutor panel knows what you\'re working on. "Guide me" for Socratic coaching, "Just tell me" for direct answers.' },
];

export default function OnboardingModal() {
  const [open, setOpen] = useState(false);
  const [step, setStep] = useState(0);
  const navigate = useNavigate();

  useEffect(() => {
    if (!localStorage.getItem(STORAGE_KEY)) setOpen(true);
  }, []);

  function dismiss(goLearn = false) {
    localStorage.setItem(STORAGE_KEY, "1");
    setOpen(false);
    if (goLearn) navigate("/");
  }

  if (!open) return null;

  const cur    = STEPS[step];
  const isLast = step === STEPS.length - 1;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 px-4">
      <div className="relative w-full max-w-md bg-[#111128] border border-violet-400/30 rounded-lg shadow-[0_0_50px_rgba(139,92,246,0.25)] overflow-hidden">

        {/* Neon top accent */}
        <div className="absolute inset-x-0 top-0 h-px bg-gradient-to-r from-transparent via-violet-400 to-transparent" />

        {/* Progress dots */}
        <div className="flex gap-1.5 justify-center pt-7">
          {STEPS.map((_, i) => (
            <div key={i} className={`h-1 rounded-full transition-all duration-300 ${
              i === step ? "w-8 bg-violet-400 shadow-[0_0_8px_rgba(139,92,246,0.6)]" : i < step ? "w-2 bg-violet-700" : "w-2 bg-violet-400/15"
            }`} />
          ))}
        </div>

        {/* Content */}
        <div className="px-8 py-8 text-center space-y-4">
          <div className="text-5xl">{cur.icon}</div>
          <h2 className="text-xl font-bold text-violet-50">{cur.title}</h2>
          <p className="text-sm text-violet-400 leading-relaxed">{cur.body}</p>
        </div>

        {/* Actions */}
        <div className="px-8 pb-8 flex items-center gap-3">
          <button onClick={() => dismiss(false)}
            className="flex-1 py-2.5 rounded-lg text-sm text-violet-500/70 hover:text-violet-200 transition-colors">
            Skip
          </button>
          {step > 0 && (
            <button onClick={() => setStep((s) => s - 1)}
              className="px-4 py-2.5 rounded-lg text-sm bg-[#150830] border border-violet-400/20 text-violet-200 hover:border-violet-400/50 transition-all">
              Back
            </button>
          )}
          <button
            onClick={() => (isLast ? dismiss(true) : setStep((s) => s + 1))}
            className="flex-1 py-2.5 rounded-lg text-sm font-semibold bg-violet-500 hover:bg-violet-400 text-white transition-all shadow-[0_0_14px_rgba(139,92,246,0.5)]"
          >
            {isLast ? "Start Learning" : "Next"}
          </button>
        </div>
      </div>
    </div>
  );
}
