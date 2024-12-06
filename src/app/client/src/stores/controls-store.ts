import create from "zustand";
import { devtools } from "zustand/middleware";
import { persist } from "zustand/middleware";

interface ControlsState {
  isOfflineFeeder: boolean;
  isFeedersStarted: boolean;
  isFeedersPaused: boolean;
  setIsOfflineFeeder: (value: boolean) => void;
  setIsFeedersStarted: (value: boolean) => void;
  setIsFeedersPaused: (value: boolean) => void;
}

export const useControlsStore = create<ControlsState>()(
  persist(
    devtools(
      (set) => ({
        isOfflineFeeder: true,
        isFeedersStarted: false,
        isFeedersPaused: false,
        setIsOfflineFeeder: (value) => set({ isOfflineFeeder: value }),
        setIsFeedersStarted: (value) => set({ isFeedersStarted: value }),
        setIsFeedersPaused: (value) => set({ isFeedersPaused: value }),
      }),
      { name: "controls-store" }
    ),
    { name: "controls-store" }
  )
);
