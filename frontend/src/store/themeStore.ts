import { create } from "zustand";
import { persist } from "zustand/middleware";

type Theme = "light" | "dark";

interface ThemeState {
  theme: Theme;
  toggle: () => void;
}

export const useThemeStore = create<ThemeState>()(
  persist(
    (set, get) => ({
      theme: "dark",
      toggle: () => {
        const next = get().theme === "dark" ? "light" : "dark";
        document.documentElement.classList.toggle("dark", next === "dark");
        set({ theme: next });
      },
    }),
    { name: "portfolio-theme" }
  )
);

// Apply theme on hydration
const stored = (JSON.parse(localStorage.getItem("portfolio-theme") ?? "{}") as { state?: { theme?: Theme } })?.state?.theme ?? "dark";
document.documentElement.classList.toggle("dark", stored === "dark");