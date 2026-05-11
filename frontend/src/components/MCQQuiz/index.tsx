import { useEffect, useState } from "react";
import { postJSON } from "../../api";
import { useStore } from "../../store";
import { playSound } from "../../sounds";

interface Question {
  id: string;
  topic: string;
  question: string;
  options: string[];
  answer: string;
  explanation: string;
  incorrect_explanations?: Record<string, string>;
}

interface Props {
  questions: Question[];
  topic: string;
  onComplete: (correct: number, total: number) => void;
}

export default function MCQQuiz({ questions, topic, onComplete }: Props) {
  const [index,    setIndex]    = useState(0);
  const [answers,  setAnswers]  = useState<Record<number, string>>({});
  const [revealed, setRevealed] = useState<Record<number, boolean>>({});
  const [finished, setFinished] = useState(false);
  const [shaking,  setShaking]  = useState(false);
  const [popping,  setPopping]  = useState(false);
  const setTutorContext = useStore((s) => s.setTutorContext);

  const q       = questions[index];

  useEffect(() => {
    if (q) {
      setTutorContext({
        mcq_question: `${q.question}\nOptions: ${q.options.join(" | ")}`,
      });
    }
  }, [index, q]);
  const chosen  = answers[index];
  const isRight = chosen === q?.answer;
  const shown   = revealed[index];

  function pick(option: string) {
    if (revealed[index]) return;
    setAnswers((a) => ({ ...a, [index]: option }));
  }

  async function submit() {
    if (!chosen || revealed[index]) return;
    const correct = chosen === q.answer;
    setRevealed((r) => ({ ...r, [index]: true }));
    if (correct) {
      playSound("correct");
      setPopping(true);
      setTimeout(() => setPopping(false), 400);
    } else {
      playSound("wrong");
      setShaking(true);
      setTimeout(() => setShaking(false), 500);
    }
    postJSON("/practice/mcq/result", {
      mcq_id:      q.id,
      topic:       q.topic || topic,
      correct,
      question_id: q.id,
    }).catch(() => {});
  }

  function next() {
    if (index < questions.length - 1) {
      setIndex(index + 1);
    } else {
      setFinished(true);
      const correct = questions.filter((_, i) => answers[i] === questions[i].answer).length;
      onComplete(correct, questions.length);
    }
  }

  function prev() {
    if (index > 0) setIndex(index - 1);
  }

  if (finished) {
    const correct = questions.filter((_, i) => answers[i] === questions[i].answer).length;
    const pct     = Math.round((correct / questions.length) * 100);
    return (
      <div className="text-center space-y-4 py-8">
        <p className="text-4xl font-bold text-violet-300">{pct}%</p>
        <p className="text-violet-200">{correct} / {questions.length} correct</p>
        <div className={`inline-block px-4 py-1 rounded-full text-sm font-medium ${
          pct >= 80 ? "bg-emerald-900/40 text-emerald-400" :
          pct >= 60 ? "bg-yellow-900/40 text-yellow-400" :
                      "bg-red-900/40 text-red-400"
        }`}>
          {pct >= 80 ? "Great work!" : pct >= 60 ? "Keep practising" : "Needs more review"}
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Progress bar + jump buttons */}
      <div className="space-y-3">
        <div className="flex items-center justify-between text-xs text-violet-500/70">
          <span>Question {index + 1} of {questions.length}</span>
          <span>{Object.keys(revealed).length} answered</span>
        </div>
        <div className="h-1 bg-violet-400/10 rounded-full overflow-hidden">
          <div
            className="h-full bg-violet-500 rounded-full transition-all"
            style={{ width: `${((index + 1) / questions.length) * 100}%` }}
          />
        </div>
        <div className="flex flex-wrap gap-1 pt-1">
          {questions.map((_, i) => (
            <button
              key={i}
              onClick={() => setIndex(i)}
              className={`w-7 h-7 text-xs rounded font-medium transition-all border ${
                i === index
                  ? "bg-violet-600 text-violet-50 border-violet-400 shadow-[0_0_8px_rgba(139,92,246,0.4)]"
                  : revealed[i]
                    ? answers[i] === questions[i].answer
                      ? "bg-emerald-800/60 text-emerald-300 border-emerald-700/50"
                      : "bg-red-800/60 text-red-300 border-red-700/50"
                    : "bg-[#150830] text-violet-400 border-violet-400/15 hover:border-violet-400/40"
              }`}
            >
              {i + 1}
            </button>
          ))}
        </div>
      </div>

      {/* Question */}
      <div className={`glass p-6 space-y-5 ${shaking ? "shake" : ""} ${popping ? "correct-pop" : ""}`}>
        <p className="text-violet-50 font-medium leading-relaxed">{q.question}</p>

        <div className="space-y-3">
          {q.options.map((opt, oi) => {
            const stagger = ["d-50","d-100","d-150","d-200"];
            let style = "bg-[#150830] text-violet-200 hover:bg-violet-400/12 border-violet-400/15 hover:border-violet-400/50 hover:text-white hover:translate-x-1";
            if (shown) {
              if (opt === q.answer)              style = "bg-emerald-900/40 text-emerald-300 border-emerald-600/60 shadow-[0_0_8px_rgba(52,211,153,0.15)]";
              else if (opt === chosen)           style = "bg-red-900/40 text-red-300 border-red-600/60";
              else                               style = "bg-[#0a0420] text-violet-600/70 border-violet-400/10";
            } else if (opt === chosen) {
              style = "bg-violet-500/20 text-violet-100 border-violet-400 shadow-[0_0_10px_rgba(139,92,246,0.25)]";
            }

            return (
              <button
                key={opt}
                onClick={() => pick(opt)}
                className={`card-enter ${stagger[oi] ?? ""} w-full text-left px-4 py-3 rounded-lg border text-sm transition-all duration-150 ${style} ${shown ? "cursor-default" : "cursor-pointer"}`}
              >
                {opt}
              </button>
            );
          })}
        </div>

        {/* Explanation */}
        {shown && (
          <div className={`rounded-lg p-4 text-sm ${isRight ? "bg-emerald-900/30 border border-emerald-800 text-emerald-200" : "bg-red-900/30 border border-red-800 text-red-200"}`}>
            <p className="font-semibold mb-1">{isRight ? "Correct!" : `Incorrect — the answer is: ${q.answer}`}</p>
            <p className="text-violet-200">{isRight ? q.explanation : (q.incorrect_explanations?.[chosen] || q.explanation)}</p>
          </div>
        )}
      </div>

      {/* Controls */}
      <div className="flex gap-3">
        <button onClick={prev} disabled={index === 0}
          className="px-4 py-2 bg-[#150830] border border-violet-400/20 hover:border-violet-400/50 disabled:opacity-30 rounded-lg text-sm font-medium transition-all">
          Previous
        </button>

        {!shown ? (
          <button onClick={submit} disabled={!chosen}
            className="px-4 py-2 bg-violet-500 hover:bg-violet-400 disabled:opacity-30 rounded-lg text-sm font-medium transition-all shadow-[0_0_10px_rgba(139,92,246,0.4)]">
            Check Answer
          </button>
        ) : (
          <button onClick={next}
            className="px-4 py-2 bg-violet-500 hover:bg-violet-400 rounded-lg text-sm font-medium transition-all shadow-[0_0_10px_rgba(139,92,246,0.4)]">
            {index < questions.length - 1 ? "Next Question" : "Finish Quiz"}
          </button>
        )}
      </div>
    </div>
  );
}
