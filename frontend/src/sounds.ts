// Retro 8-bit sound effects — all synthesized via Web Audio API, no audio files
type SoundName = "navigate" | "click" | "correct" | "wrong" | "send" | "run" | "pass" | "fail";

let _ctx: AudioContext | null = null;

function ac(): AudioContext {
  if (!_ctx) _ctx = new (window.AudioContext || (window as unknown as { webkitAudioContext: typeof AudioContext }).webkitAudioContext)();
  return _ctx;
}

function tone(
  freq: number,
  startOffset: number,
  duration: number,
  type: OscillatorType = "square",
  gainPeak = 0.08,
) {
  const ctx = ac();
  const osc  = ctx.createOscillator();
  const gain = ctx.createGain();
  osc.connect(gain);
  gain.connect(ctx.destination);
  osc.type = type;
  osc.frequency.setValueAtTime(freq, ctx.currentTime + startOffset);
  gain.gain.setValueAtTime(0, ctx.currentTime + startOffset);
  gain.gain.linearRampToValueAtTime(gainPeak, ctx.currentTime + startOffset + 0.005);
  gain.gain.exponentialRampToValueAtTime(0.0001, ctx.currentTime + startOffset + duration);
  osc.start(ctx.currentTime + startOffset);
  osc.stop(ctx.currentTime + startOffset + duration + 0.02);
}

const SOUNDS: Record<SoundName, () => void> = {
  // Soft two-note ascend on page nav
  navigate: () => {
    tone(523, 0,    0.06, "sine",     0.07);
    tone(659, 0.06, 0.09, "sine",     0.07);
  },
  // Single short blip for button presses
  click: () => {
    tone(440, 0, 0.045, "square", 0.055);
  },
  // Triumphant three-note arpeggio
  correct: () => {
    tone(523, 0,    0.08, "square", 0.09);
    tone(659, 0.08, 0.08, "square", 0.09);
    tone(784, 0.16, 0.16, "square", 0.10);
  },
  // Low descending buzz
  wrong: () => {
    tone(220, 0,    0.07, "sawtooth", 0.07);
    tone(165, 0.07, 0.13, "sawtooth", 0.06);
  },
  // Soft two-note ping
  send: () => {
    tone(880,  0,    0.04, "sine", 0.06);
    tone(1047, 0.04, 0.08, "sine", 0.05);
  },
  // Quick three-step ascending sweep
  run: () => {
    tone(330, 0,    0.04, "square", 0.06);
    tone(440, 0.04, 0.04, "square", 0.06);
    tone(523, 0.08, 0.05, "square", 0.06);
  },
  // Victory jingle — four ascending notes
  pass: () => {
    tone(523,  0,    0.07, "square", 0.09);
    tone(659,  0.07, 0.07, "square", 0.09);
    tone(784,  0.14, 0.07, "square", 0.09);
    tone(1047, 0.21, 0.18, "square", 0.10);
  },
  // Descending fail tone
  fail: () => {
    tone(330, 0,    0.09, "sawtooth", 0.08);
    tone(220, 0.09, 0.18, "sawtooth", 0.07);
  },
};

export function playSound(name: SoundName): void {
  try {
    SOUNDS[name]();
  } catch {
    // Browser may block AudioContext until first user gesture — fail silently
  }
}
