interface Props { onClose: () => void; }

const GROUPS = [
  {
    label: "Global",
    shortcuts: [
      { keys: ["⌘", "K"],  desc: "Open search" },
      { keys: ["?"],        desc: "Toggle this panel" },
      { keys: ["Esc"],      desc: "Close any modal" },
    ],
  },
  {
    label: "Navigation",
    shortcuts: [
      { keys: ["G", "L"], desc: "Go to Learn" },
      { keys: ["G", "P"], desc: "Go to Practice" },
      { keys: ["G", "I"], desc: "Go to Interview" },
      { keys: ["G", "D"], desc: "Go to Dashboard" },
    ],
  },
  {
    label: "Tutor sidebar",
    shortcuts: [
      { keys: ["⌘", "\\"], desc: "Toggle tutor sidebar" },
    ],
  },
];

function Key({ k }: { k: string }) {
  return (
    <kbd className="inline-flex items-center justify-center min-w-[1.6rem] h-6 px-1.5 text-xs font-mono bg-violet-400/10 border border-violet-400/25 rounded text-violet-200">
      {k}
    </kbd>
  );
}

export default function KeyboardShortcutsModal({ onClose }: Props) {
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/75" onClick={onClose}>
      <div
        className="w-full max-w-sm bg-[#111128] border border-violet-400/30 rounded-lg shadow-[0_0_40px_rgba(139,92,246,0.2)] overflow-hidden"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="flex items-center justify-between px-5 py-4 border-b border-violet-400/15">
          <h2 className="text-sm font-semibold text-violet-200">Keyboard Shortcuts</h2>
          <button onClick={onClose} className="text-violet-500/70 hover:text-violet-200 text-xl leading-none transition-colors">×</button>
        </div>
        <div className="p-5 space-y-5">
          {GROUPS.map((g) => (
            <div key={g.label}>
              <p className="text-xs text-violet-600/70 uppercase tracking-widest mb-2.5">{g.label}</p>
              <div className="space-y-3.5">
                {g.shortcuts.map((s, i) => (
                  <div key={i} className="flex items-center justify-between">
                    <span className="text-sm text-violet-200">{s.desc}</span>
                    <div className="flex items-center gap-1">
                      {s.keys.map((k, j) => <Key key={j} k={k} />)}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
