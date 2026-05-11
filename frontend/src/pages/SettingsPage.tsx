import { useEffect, useState } from "react";
import { fetchJSON, postJSON } from "../api";
import { useStore } from "../store";

interface PlatformStatus {
  api_model: string; rag_enabled: boolean;
  content_courses: number; content_problems: number; content_mcq_tests: number;
}

interface ResetAction { key: string; label: string; desc: string; danger?: boolean; }

const RESETS: ResetAction[] = [
  { key: "progress",          label: "Reset learning progress",  desc: "Clears topic scores, completed courses & problems, activity history." },
  { key: "interview",         label: "Clear interview history",  desc: "Deletes the saved conversation from the last mock interview." },
  { key: "spaced-repetition", label: "Reset spaced repetition", desc: "Clears all SM-2 review cards — questions will start fresh." },
  { key: "notes",             label: "Delete all notes",         desc: "Permanently removes every lesson note you've written." },
  { key: "all",               label: "Reset everything",         desc: "Wipes all of the above at once.", danger: true },
];

export default function SettingsPage() {
  const [status,     setStatus]     = useState<PlatformStatus | null>(null);
  const [confirming, setConfirming] = useState<string | null>(null);
  const [toast,      setToast]      = useState("");
  const [reindexing, setReindexing] = useState(false);
  const { socraticMode, setSocraticMode } = useStore();

  useEffect(() => {
    fetchJSON<PlatformStatus>("/settings/status").then(setStatus).catch(console.error);
  }, []);

  function showToast(msg: string) { setToast(msg); setTimeout(() => setToast(""), 3500); }

  async function doReset(key: string) {
    try { await postJSON(`/settings/reset/${key}`, {}); showToast(`Reset "${key}" complete.`); }
    catch { showToast("Reset failed — check the server."); }
    setConfirming(null);
  }

  async function doReindex() {
    setReindexing(true);
    try { await postJSON("/settings/reindex", {}); showToast("Re-indexing started in the background."); }
    catch { showToast("Re-index failed — check the server."); }
    finally { setReindexing(false); }
  }

  async function exportNotes() {
    try {
      const data = await fetchJSON<{ markdown: string }>("/notes/export");
      const url  = URL.createObjectURL(new Blob([data.markdown], { type: "text/markdown" }));
      const a    = Object.assign(document.createElement("a"), { href: url, download: "my-notes.md" });
      a.click(); URL.revokeObjectURL(url);
    } catch { showToast("Export failed."); }
  }

  return (
    <div className="max-w-xl space-y-8">
      <h1 className="text-2xl font-bold text-violet-50">Settings</h1>

      {toast && (
        <div className="fixed top-4 right-4 z-50 bg-emerald-500/20 border border-emerald-500/30 text-emerald-300 text-sm px-4 py-2.5 rounded-lg shadow-[0_0_20px_rgba(52,211,153,0.2)]">
          {toast}
        </div>
      )}

      {/* Platform status */}
      <Section title="Platform Status">
        <div className="glass divide-y divide-violet-400/10">
          {status ? (
            <>
              <Row label="AI Model"       value={status.api_model} />
              <Row label="RAG / Search"   value={status.rag_enabled ? "Indexed ✓" : "Not indexed"} tag={status.rag_enabled ? "green" : "amber"} />
              <Row label="Courses"        value={String(status.content_courses)} />
              <Row label="Problems"       value={String(status.content_problems)} />
              <Row label="MCQ Test banks" value={String(status.content_mcq_tests)} />
            </>
          ) : (
            <p className="px-4 py-3 text-sm text-violet-500/70">Loading…</p>
          )}
        </div>
      </Section>

      {/* Content & RAG */}
      <Section title="Content & RAG">
        <div className="glass divide-y divide-violet-400/10">
          <ActionRow
            label="Re-index course content"
            desc="Rebuild the AI tutor's knowledge base from all course files."
            btn={reindexing ? "Starting…" : "Re-index"}
            onClick={doReindex}
            disabled={reindexing}
          />
          <ActionRow
            label="Export all notes"
            desc="Download your lesson notes as a single Markdown file."
            btn="↓ Download"
            onClick={exportNotes}
          />
        </div>
      </Section>

      {/* Tutor preference */}
      <Section title="Tutor Preference">
        <div className="glass p-5 flex items-center justify-between gap-4">
          <div>
            <p className="text-sm font-medium text-violet-100">Default mode</p>
            <p className="text-xs text-violet-500/70 mt-0.5">
              {socraticMode ? "Guide me — tutor asks questions." : "Direct — tutor answers plainly."}
            </p>
          </div>
          <div className="flex gap-3 shrink-0">
            <ModeBtn active={socraticMode}  onClick={() => setSocraticMode(true)}  label="Guide me" />
            <ModeBtn active={!socraticMode} onClick={() => setSocraticMode(false)} label="Direct" />
          </div>
        </div>
      </Section>

      {/* Data resets */}
      <Section title="Data Management">
        <div className="glass divide-y divide-violet-400/10">
          {RESETS.map((r) => (
            <div key={r.key} className="px-4 py-3.5 flex items-center justify-between gap-4">
              <div className="min-w-0">
                <p className={`text-sm font-medium ${r.danger ? "text-red-400" : "text-violet-100"}`}>{r.label}</p>
                <p className="text-xs text-violet-500/70 mt-0.5">{r.desc}</p>
              </div>
              {confirming === r.key ? (
                <div className="flex gap-3 shrink-0">
                  <button onClick={() => doReset(r.key)}
                    className="px-3 py-1 rounded-lg text-xs font-medium bg-red-500/80 hover:bg-red-500 text-white transition-colors">
                    Confirm
                  </button>
                  <button onClick={() => setConfirming(null)}
                    className="px-3 py-1 rounded-lg text-xs font-medium bg-[#150830] hover:bg-violet-400/10 text-violet-200 border border-violet-400/20 transition-all">
                    Cancel
                  </button>
                </div>
              ) : (
                <button onClick={() => setConfirming(r.key)}
                  className={`shrink-0 px-3 py-1 rounded-lg text-xs font-medium border transition-colors ${
                    r.danger
                      ? "bg-red-500/10 border-red-500/20 text-red-400 hover:bg-red-500/20"
                      : "bg-[#150830] border-violet-400/20 text-violet-400 hover:text-violet-100 hover:border-violet-400/50"
                  }`}>
                  Reset
                </button>
              )}
            </div>
          ))}
        </div>
      </Section>
    </div>
  );
}

function Section({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <section>
      <h2 className="text-xs font-semibold text-violet-500/70 uppercase tracking-widest mb-5">{title}</h2>
      {children}
    </section>
  );
}

function Row({ label, value, tag }: { label: string; value: string; tag?: "green" | "amber" }) {
  return (
    <div className="px-4 py-3 flex items-center justify-between">
      <p className="text-sm text-violet-400">{label}</p>
      <p className={`text-sm font-medium ${tag === "green" ? "text-emerald-400" : tag === "amber" ? "text-violet-400" : "text-violet-100"}`}>
        {value}
      </p>
    </div>
  );
}

function ActionRow({ label, desc, btn, onClick, disabled }: { label: string; desc: string; btn: string; onClick: () => void; disabled?: boolean; }) {
  return (
    <div className="px-4 py-3.5 flex items-center justify-between gap-4">
      <div>
        <p className="text-sm font-medium text-violet-100">{label}</p>
        <p className="text-xs text-violet-500/70 mt-0.5">{desc}</p>
      </div>
      <button onClick={onClick} disabled={disabled}
        className="shrink-0 px-3 py-1.5 rounded-lg text-xs font-medium bg-[#150830] border border-violet-400/20 text-violet-200 hover:border-violet-400/50 disabled:opacity-50 transition-all">
        {btn}
      </button>
    </div>
  );
}

function ModeBtn({ active, onClick, label }: { active: boolean; onClick: () => void; label: string }) {
  return (
    <button onClick={onClick}
      className={`px-3 py-1.5 rounded-xl text-xs font-medium transition-all ${
        active
          ? "bg-violet-600 text-violet-50 border border-violet-400/50 shadow-[0_0_10px_rgba(139,92,246,0.4)]"
          : "bg-[#150830] border border-violet-400/20 text-violet-400 hover:text-violet-100 hover:border-violet-400/50"
      }`}>
      {label}
    </button>
  );
}
