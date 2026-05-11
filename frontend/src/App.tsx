import { useEffect, useRef, useState } from "react";
import { Routes, Route, NavLink, useNavigate, useLocation } from "react-router-dom";
import { playSound } from "./sounds";
import LearnPage              from "./pages/LearnPage";
import PracticePage           from "./pages/PracticePage";
import InterviewPage          from "./pages/InterviewPage";
import DashboardPage          from "./pages/DashboardPage";
import SettingsPage           from "./pages/SettingsPage";
import TutorSidebar           from "./components/TutorSidebar";
import SearchModal            from "./components/SearchModal";
import OnboardingModal        from "./components/OnboardingModal";
import KeyboardShortcutsModal from "./components/KeyboardShortcutsModal";

const NAV_ITEMS = [
  { to: "/dashboard", label: "Dashboard", icon: "📊", key: "d" },
  { to: "/",          label: "Learn",     icon: "📖", key: "l" },
  { to: "/practice",  label: "Practice",  icon: "⚡", key: "p" },
  { to: "/interview", label: "Interview", icon: "🎯", key: "i" },
  { to: "/settings",  label: "Settings",  icon: "⚙️", key: "s" },
];

/* ── Logo mark SVG ── */
function LogoMark({ size = 28 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 32 32" xmlns="http://www.w3.org/2000/svg" className="shrink-0">
      <rect width="32" height="32" fill="#0d0820"/>
      <rect x="1.5" y="1.5" width="29" height="29" rx="2" fill="none" stroke="#8b5cf6" strokeWidth="1.5"/>
      {/* Neural connections */}
      <line x1="7"  y1="9"  x2="16" y2="16" stroke="#4c1d95" strokeWidth="1.2"/>
      <line x1="25" y1="9"  x2="16" y2="16" stroke="#4c1d95" strokeWidth="1.2"/>
      <line x1="7"  y1="23" x2="16" y2="16" stroke="#4c1d95" strokeWidth="1.2"/>
      <line x1="25" y1="23" x2="16" y2="16" stroke="#4c1d95" strokeWidth="1.2"/>
      <line x1="4"  y1="16" x2="16" y2="16" stroke="#3b0764" strokeWidth="1"/>
      <line x1="28" y1="16" x2="16" y2="16" stroke="#3b0764" strokeWidth="1"/>
      {/* Outer nodes */}
      <circle cx="7"  cy="9"  r="2"   fill="#6d28d9"/>
      <circle cx="25" cy="9"  r="2"   fill="#6d28d9"/>
      <circle cx="7"  cy="23" r="2"   fill="#6d28d9"/>
      <circle cx="25" cy="23" r="2"   fill="#6d28d9"/>
      <circle cx="4"  cy="16" r="1.5" fill="#4c1d95"/>
      <circle cx="28" cy="16" r="1.5" fill="#4c1d95"/>
      {/* Centre node */}
      <circle cx="16" cy="16" r="3.5" fill="#8b5cf6"/>
      <circle cx="16" cy="16" r="2"   fill="#c4b5fd"/>
      {/* Amber spark */}
      <circle cx="26.5" cy="5.5" r="2.5" fill="#f59e0b"/>
      <circle cx="26.5" cy="5.5" r="1.2" fill="#fef3c7"/>
    </svg>
  );
}

export default function App() {
  const [searching, setSearching] = useState(false);
  const [shortcuts, setShortcuts] = useState(false);
  const [navOpen,   setNavOpen]   = useState(false);
  const [tutorOpen, setTutorOpen] = useState(true);
  const gPending = useRef<string | null>(null);
  const navigate = useNavigate();

  useEffect(() => {
    function onKey(e: KeyboardEvent) {
      const tag = (e.target as HTMLElement).tagName;
      const inField = tag === "INPUT" || tag === "TEXTAREA" || (e.target as HTMLElement).isContentEditable;

      if ((e.metaKey || e.ctrlKey) && e.key === "k")  { e.preventDefault(); setSearching((s) => !s); return; }
      if ((e.metaKey || e.ctrlKey) && e.key === "\\") { e.preventDefault(); setTutorOpen((o) => !o); return; }
      if (inField) return;
      if (e.key === "?")      { setShortcuts((s) => !s); return; }
      if (e.key === "Escape") { setSearching(false); setShortcuts(false); setNavOpen(false); return; }
      if (e.key.toLowerCase() === "g") { gPending.current = "g"; return; }
      if (gPending.current === "g") {
        gPending.current = null;
        const item = NAV_ITEMS.find((n) => n.key === e.key.toLowerCase());
        if (item) navigate(item.to);
        return;
      }
      gPending.current = null;
    }
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [navigate]);

  const location = useLocation();

  return (
    <div className="flex h-screen overflow-hidden">

      {/* Mobile overlay */}
      {navOpen && (
        <div className="fixed inset-0 z-30 bg-black/80 lg:hidden" onClick={() => setNavOpen(false)} />
      )}

      {/* ── Left nav ── */}
      <nav className={`
        fixed lg:static z-40 inset-y-0 left-0 w-56 shrink-0
        glass-dark border-r border-[#1e0a40]
        flex flex-col gap-2 p-5
        transition-transform duration-200
        ${navOpen ? "translate-x-0" : "-translate-x-full lg:translate-x-0"}
      `}>
        {/* Logo */}
        <div className="flex items-center justify-between px-1 mb-8 pt-2">
          <div className="flex items-center gap-3">
            <LogoMark size={32} />
            <div className="flex flex-col gap-1">
              <span className="pixel text-[11px] text-violet-300 leading-none tracking-wider glow-text">
                ED-AI
              </span>
              <span className="text-[8px] text-violet-700/70 tracking-[0.18em] uppercase">RPG Edition</span>
            </div>
          </div>
          <button onClick={() => setNavOpen(false)} className="lg:hidden text-violet-600/60 hover:text-violet-300 text-xl">×</button>
        </div>

        {/* Search */}
        <button
          onClick={() => { setSearching(true); setNavOpen(false); }}
          className="flex items-center gap-2.5 px-3 py-3 mb-2 text-violet-600/60 hover:text-violet-300 hover:bg-violet-400/8 border-2 border-dashed border-violet-800/60 hover:border-violet-500/50 transition-all w-full text-left"
          style={{ borderRadius: 2 }}
        >
          <span className="text-sm">🔍</span>
          <span className="pixel text-[7px] tracking-wider">SEARCH</span>
          <kbd className="ml-auto text-[7px] bg-violet-400/8 border border-violet-700/40 px-1.5 py-0.5 text-violet-600 hidden sm:block" style={{ borderRadius: 2 }}>⌘K</kbd>
        </button>

        {/* Nav links */}
        {NAV_ITEMS.map(({ to, label, icon }) => (
          <NavLink
            key={to}
            to={to}
            end={to === "/dashboard"}
            onClick={() => { setNavOpen(false); playSound("navigate"); }}
            className={({ isActive }) =>
              `flex items-center gap-3 px-3 py-3.5 font-medium transition-all duration-150 border-l-4 border-r border-b border-t ${
                isActive
                  ? "border-l-violet-400 border-r-violet-800/40 border-y-violet-800/40 bg-violet-400/10 text-violet-200 shadow-[0_0_16px_rgba(139,92,246,0.15)]"
                  : "border-l-transparent border-r-transparent border-y-transparent text-violet-600/70 hover:border-l-violet-700 hover:text-violet-300 hover:bg-violet-400/5"
              }`
            }
          >
            <span className="text-base shrink-0">{icon}</span>
            <span className="pixel text-[7px] tracking-wider">{label.toUpperCase()}</span>
          </NavLink>
        ))}

        {/* Divider */}
        <div className="my-3 border-t border-dashed border-violet-900/60" />

        {/* AI Tutor toggle */}
        <button
          onClick={() => { setTutorOpen((o) => !o); setNavOpen(false); playSound("click"); }}
          className={`flex items-center gap-3 px-3 py-3.5 border-l-4 border-r border-b border-t transition-all ${
            tutorOpen
              ? "border-l-amber-500 border-r-amber-900/30 border-y-amber-900/30 bg-amber-500/8 text-amber-300 shadow-[0_0_14px_rgba(245,158,11,0.15)]"
              : "border-l-transparent border-r-transparent border-y-transparent text-violet-600/70 hover:border-l-violet-700 hover:text-violet-300 hover:bg-violet-400/5"
          }`}
        >
          <span className="text-base">🧠</span>
          <span className="pixel text-[7px] tracking-wider">AI TUTOR</span>
          <span className="ml-auto text-xs opacity-50">{tutorOpen ? "◀" : "▶"}</span>
        </button>

        {/* Shortcuts */}
        <button
          onClick={() => { setShortcuts(true); setNavOpen(false); }}
          className="mt-auto flex items-center gap-2 px-3 py-2.5 text-violet-800/70 hover:text-violet-500 transition-colors w-full text-left"
        >
          <kbd className="text-[7px] bg-violet-400/8 border border-violet-800/50 px-1.5 py-0.5 text-violet-600 pixel" style={{ borderRadius: 2 }}>?</kbd>
          <span className="pixel text-[6px] tracking-wider">SHORTCUTS</span>
        </button>
      </nav>

      {/* ── Main area ── */}
      <div className="flex flex-1 overflow-hidden min-w-0">
        <div className="flex-1 flex flex-col overflow-hidden min-w-0">

          {/* Mobile top bar */}
          <div className="flex items-center gap-3 px-5 py-4 border-b border-[#1e0a40] bg-[#040210] lg:hidden">
            <button onClick={() => setNavOpen(true)} className="text-violet-500/70 hover:text-violet-300 text-xl">☰</button>
            <LogoMark size={22} />
            <span className="pixel text-[9px] text-violet-400 glow-text">ED-AI</span>
            <button
              onClick={() => setTutorOpen((o) => !o)}
              className={`ml-auto pixel text-[7px] px-3 py-1.5 border-2 transition-all ${
                tutorOpen
                  ? "border-amber-500/50 bg-amber-500/8 text-amber-300"
                  : "border-violet-800/50 text-violet-600/60 hover:text-violet-300"
              }`}
              style={{ borderRadius: 2 }}
            >
              {tutorOpen ? "HIDE" : "TUTOR"}
            </button>
          </div>

          <main className="flex-1 overflow-y-auto p-7 lg:p-12">
            <div key={location.pathname} className="page-enter h-full">
              <Routes>
                <Route path="/"          element={<LearnPage />}     />
                <Route path="/practice"  element={<PracticePage />}  />
                <Route path="/interview" element={<InterviewPage />} />
                <Route path="/dashboard" element={<DashboardPage />} />
                <Route path="/settings"  element={<SettingsPage />}  />
              </Routes>
            </div>
          </main>
        </div>

        {/* Tutor sidebar */}
        {tutorOpen && <TutorSidebar onClose={() => setTutorOpen(false)} />}
      </div>

      {/* Modals */}
      {searching && <SearchModal            onClose={() => setSearching(false)} />}
      {shortcuts && <KeyboardShortcutsModal onClose={() => setShortcuts(false)} />}
      <OnboardingModal />
    </div>
  );
}
