import { create } from "zustand";

interface TutorContext {
  page: string;
  course_id?: string;
  course_title?: string;
  current_topic?: string;
  problem_id?: string;
  problem_title?: string;
  problem_description?: string;
  user_code?: string;
  failed_tests?: unknown[];
  mcq_question?: string;
}

interface AppState {
  socraticMode: boolean;
  setSocraticMode: (val: boolean) => void;

  tutorContext: TutorContext;
  setTutorContext: (ctx: Partial<TutorContext>) => void;
}

export const useStore = create<AppState>((set) => ({
  socraticMode: true,
  setSocraticMode: (val) => set({ socraticMode: val }),

  tutorContext: { page: "general" },
  setTutorContext: (ctx) =>
    set((s) => ({ tutorContext: { ...s.tutorContext, ...ctx } })),
}));
