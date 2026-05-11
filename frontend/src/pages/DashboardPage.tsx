import { useEffect, useRef, useState } from "react";
import { fetchJSON } from "../api";
import { useStore } from "../store";

interface DayActivity {
  date: string; problems: number; mcqs: number; messages: number; total: number;
}
interface TopicStat {
  topic: string; seen: number; correct: number; accuracy: number;
}
interface Stats {
  streak: number; week: DayActivity[];
  completed_courses: number; completed_problems: number; completed_mcqs: number;
  topics: Record<string, { seen: number; correct: number; accuracy: number }>;
  weak_topics: TopicStat[]; strong_topics: TopicStat[];
}
interface RecommendedProblem { id: string; title: string; difficulty: string; topics: string[]; reason: string; }
interface RecommendedCourse  { id: string; title: string; difficulty: string; reason: string; }
interface Recommendations    { problems: RecommendedProblem[]; courses: RecommendedCourse[]; }

const DIFF_COLOR: Record<string, string> = {
  easy: "text-emerald-400", medium: "text-yellow-400", hard: "text-red-400",
  beginner: "text-emerald-400", intermediate: "text-yellow-400", advanced: "text-red-400",
};

function dayLabel(iso: string) {
  return new Date(iso + "T00:00:00").toLocaleDateString("en-US", { weekday: "short" });
}

// ── Milestone badges ──────────────────────────────────────────────────────────

interface Milestone { icon: string; label: string; achieved: boolean; }

function milestones(s: Stats): Milestone[] {
  return [
    { icon: "🌱", label: "First day",       achieved: s.streak >= 1 },
    { icon: "🔥", label: "3-day streak",    achieved: s.streak >= 3 },
    { icon: "⚡", label: "Week warrior",    achieved: s.streak >= 7 },
    { icon: "🏆", label: "30-day legend",   achieved: s.streak >= 30 },
    { icon: "💡", label: "First problem",   achieved: s.completed_problems >= 1 },
    { icon: "🧩", label: "Problem solver",  achieved: s.completed_problems >= 5 },
    { icon: "🎓", label: "Course complete", achieved: s.completed_courses >= 1 },
    { icon: "📚", label: "Avid learner",    achieved: s.completed_courses >= 3 },
    { icon: "🎯", label: "MCQ master",      achieved: s.completed_mcqs >= 20 },
  ];
}

function MilestoneBadge({ m, delay = "" }: { m: Milestone; delay?: string }) {
  return (
    <div className={`card-enter ${delay} flex flex-col items-center gap-1.5 p-3 rounded-lg border transition-all duration-200 ${
      m.achieved
        ? "border-violet-400/40 bg-violet-400/10 shadow-[0_0_12px_rgba(139,92,246,0.2)] hover:border-violet-300/65 hover:shadow-[0_0_20px_rgba(139,92,246,0.3)] hover:-translate-y-1"
        : "border-violet-400/10 bg-[#0a0420] opacity-35 grayscale"
    }`}>
      <span className="text-2xl">{m.icon}</span>
      <span className="text-[11px] text-violet-400 text-center leading-tight">{m.label}</span>
    </div>
  );
}

// ── Count-up hook ─────────────────────────────────────────────────────────────

function useCountUp(target: number, duration = 900) {
  const [display, setDisplay] = useState(0);
  const rafRef = useRef<number>();
  useEffect(() => {
    const start = performance.now();
    function tick(now: number) {
      const t = Math.min((now - start) / duration, 1);
      const eased = 1 - Math.pow(1 - t, 3);
      setDisplay(Math.round(eased * target));
      if (t < 1) rafRef.current = requestAnimationFrame(tick);
    }
    rafRef.current = requestAnimationFrame(tick);
    return () => { if (rafRef.current) cancelAnimationFrame(rafRef.current); };
  }, [target]);
  return display;
}

// ── Sub-components ────────────────────────────────────────────────────────────

function StatCard({ label, value, sub, delay = "" }: { label: string; value: number; sub?: string; delay?: string }) {
  const displayed = useCountUp(value);
  return (
    <div className={`glass card-hover p-6 text-center stat-enter ${delay}`}>
      <p className="pixel text-2xl text-violet-400 glow-text mb-3">
        {displayed}
      </p>
      <p className="pixel text-[7px] text-violet-600/80 leading-relaxed tracking-wide">{label.toUpperCase()}</p>
      {sub && <p className="text-[10px] text-violet-700/60 mt-2">{sub}</p>}
    </div>
  );
}

function ActivityBar({ day, max }: { day: DayActivity; max: number }) {
  const pct     = max > 0 ? (day.total / max) * 100 : 0;
  const isToday = day.date === new Date().toISOString().slice(0, 10);
  return (
    <div className="flex flex-col items-center gap-1.5 flex-1">
      <div className="w-full flex flex-col justify-end" style={{ height: 60 }}>
        <div
          className={`w-full rounded-t transition-all ${
            isToday
              ? "bg-gradient-to-t from-violet-500 to-violet-300 shadow-lg shadow-violet-900/40"
              : "bg-white/20"
          }`}
          style={{ height: `${Math.max(pct, day.total > 0 ? 8 : 0)}%` }}
          title={`${day.total} actions`}
        />
      </div>
      <span className={`text-xs ${isToday ? "text-violet-300 font-medium" : "text-violet-600/70"}`}>
        {dayLabel(day.date)}
      </span>
    </div>
  );
}

function TopicBar({ topic, seen, correct, accuracy }: TopicStat) {
  const pct   = Math.round(accuracy * 100);
  const color = accuracy >= 0.8 ? "from-emerald-500 to-emerald-400"
              : accuracy >= 0.6 ? "from-yellow-500 to-yellow-400"
              : "from-red-500 to-red-400";
  return (
    <div>
      <div className="flex justify-between text-xs text-violet-400 mb-1.5">
        <span className="capitalize">{topic}</span>
        <span>{pct}% <span className="text-violet-600/70">({correct}/{seen})</span></span>
      </div>
      <div className="h-1.5 bg-white/[0.07] rounded-full overflow-hidden">
        <div className={`h-full rounded-full bg-gradient-to-r ${color} transition-all`} style={{ width: `${pct}%` }} />
      </div>
    </div>
  );
}

// ── Page ──────────────────────────────────────────────────────────────────────

export default function DashboardPage() {
  const [stats, setStats] = useState<Stats | null>(null);
  const [recs,  setRecs]  = useState<Recommendations | null>(null);
  const setTutorContext   = useStore((s) => s.setTutorContext);

  useEffect(() => {
    setTutorContext({ page: "dashboard" });
    fetchJSON<Stats>("/progress/stats").then(setStats).catch(console.error);
    fetchJSON<Recommendations>("/progress/recommendations").then(setRecs).catch(console.error);
  }, []);

  if (!stats) return <p className="text-violet-500/70 text-sm">Loading…</p>;

  const maxDay    = Math.max(...stats.week.map((d) => d.total), 1);
  const allTopics = Object.entries(stats.topics).sort((a, b) => a[1].accuracy - b[1].accuracy);
  const hasActivity = stats.week.some((d) => d.total > 0);

  return (
    <div className="space-y-8 max-w-4xl">
      <h1 className="pixel text-[11px] text-violet-400 glow-text">Dashboard</h1>

      {/* Achievements */}
      <section>
        <h2 className="text-xs font-semibold text-violet-500/70 uppercase tracking-widest mb-5">Achievements</h2>
        <div className="grid grid-cols-3 sm:grid-cols-5 lg:grid-cols-9 gap-3">
          {milestones(stats).map((m, i) => {
            const delays = ["d-50","d-100","d-150","d-200","d-250","d-300","d-350","d-400","d-450"];
            return <MilestoneBadge key={m.label} m={m} delay={delays[i] ?? ""} />;
          })}
        </div>
      </section>

      {/* Stats */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
        <StatCard label="Day streak"      value={stats.streak}             sub={stats.streak > 0 ? "Keep it up!" : "Start today"} delay="d-100" />
        <StatCard label="Courses done"    value={stats.completed_courses}  delay="d-200" />
        <StatCard label="Problems solved" value={stats.completed_problems} delay="d-300" />
        <StatCard label="MCQs answered"   value={stats.completed_mcqs}     delay="d-400" />
      </div>

      {/* Activity chart */}
      <div className="glass p-6">
        <h2 className="text-sm font-semibold text-violet-200 mb-5">Activity — last 7 days</h2>
        {!hasActivity ? (
          <p className="text-violet-600/70 text-sm text-center py-6">No activity yet. Start a course or solve a problem.</p>
        ) : (
          <div className="flex gap-3 items-end">
            {stats.week.map((d) => <ActivityBar key={d.date} day={d} max={maxDay} />)}
          </div>
        )}
        {hasActivity && (
          <div className="flex gap-4 mt-3 text-xs text-violet-600/70">
            <span><span className="text-violet-300">■</span> Today</span>
            <span><span className="text-white/20">■</span> Past days</span>
          </div>
        )}
      </div>

      {/* Recommendations */}
      {recs && (recs.problems.length > 0 || recs.courses.length > 0) && (
        <div className="glass p-6">
          <h2 className="text-sm font-semibold text-violet-200 mb-5">Recommended for you</h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-5">
            {recs.problems.length > 0 && (
              <div>
                <p className="text-xs text-violet-500/70 uppercase tracking-wide mb-5">Problems</p>
                <div className="space-y-3">
                  {recs.problems.map((p) => (
                    <div key={p.id} className="flex items-start gap-4 bg-[#150830] border border-violet-400/15 rounded-lg px-4 py-3 hover:border-violet-400/40 transition-all duration-150">
                      <div className="flex-1 min-w-0">
                        <p className="text-sm text-violet-100 font-medium truncate">{p.title}</p>
                        <p className="text-xs text-violet-500/70 mt-0.5">{p.reason}</p>
                      </div>
                      <span className={`text-xs font-medium capitalize shrink-0 ${DIFF_COLOR[p.difficulty] ?? "text-violet-400"}`}>
                        {p.difficulty}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            )}
            {recs.courses.length > 0 && (
              <div>
                <p className="text-xs text-violet-500/70 uppercase tracking-wide mb-5">Courses</p>
                <div className="space-y-3">
                  {recs.courses.map((c) => (
                    <div key={c.id} className="flex items-start gap-4 bg-[#150830] border border-violet-400/15 rounded-lg px-4 py-3 hover:border-violet-400/40 transition-all duration-150">
                      <div className="flex-1 min-w-0">
                        <p className="text-sm text-violet-100 font-medium truncate">{c.title}</p>
                        <p className="text-xs text-violet-500/70 mt-0.5">{c.reason}</p>
                      </div>
                      <span className={`text-xs font-medium capitalize shrink-0 ${DIFF_COLOR[c.difficulty] ?? "text-violet-400"}`}>
                        {c.difficulty}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Topic accuracy */}
      {allTopics.length > 0 && (
        <div className="glass p-6">
          <h2 className="text-sm font-semibold text-violet-200 mb-5">Topic accuracy</h2>
          <div className="space-y-3">
            {allTopics.map(([topic, s]) => (
              <TopicBar key={topic} topic={topic} seen={s.seen} correct={s.correct} accuracy={s.accuracy} />
            ))}
          </div>
        </div>
      )}

      {/* Focus / strengths */}
      {stats.weak_topics.length > 0 && (
        <div className="bg-red-500/[0.07] border border-red-500/20 rounded-lg p-6">
          <h2 className="text-sm font-semibold text-red-400 mb-2">Focus areas</h2>
          <p className="text-xs text-violet-500/70 mb-5">Topics below 60% accuracy:</p>
          <div className="flex flex-wrap gap-3">
            {stats.weak_topics.map(({ topic, accuracy }) => (
              <span key={topic} className="text-xs bg-red-500/10 border border-red-500/20 text-red-300 px-2.5 py-1 rounded-lg capitalize">
                {topic} {Math.round(accuracy * 100)}%
              </span>
            ))}
          </div>
        </div>
      )}

      {stats.strong_topics.length > 0 && (
        <div className="bg-emerald-500/[0.07] border border-emerald-500/20 rounded-lg p-6">
          <h2 className="text-sm font-semibold text-emerald-400 mb-2">Strengths</h2>
          <div className="flex flex-wrap gap-3">
            {stats.strong_topics.map(({ topic, accuracy }) => (
              <span key={topic} className="text-xs bg-emerald-500/10 border border-emerald-500/20 text-emerald-300 px-2.5 py-1 rounded-lg capitalize">
                {topic} {Math.round(accuracy * 100)}%
              </span>
            ))}
          </div>
        </div>
      )}

      {allTopics.length === 0 && (
        <div className="text-center py-20">
          <p className="text-6xl mb-6 float-slow inline-block">📊</p>
          <p className="text-sm text-violet-600/70 mt-4">No activity yet.</p>
          <p className="text-xs mt-2 text-violet-700/50">Complete a course or solve a problem to see your stats.</p>
        </div>
      )}
    </div>
  );
}
