import create from "zustand";
import { Attack } from "../../../types/client-types";
import { devtools } from "zustand/middleware";
// import { persist } from "zustand/middleware";

interface SavedAttacksState {
  savedAttacks: Attack[];
  setSavedAttacks: (attacks: Attack[]) => void;
  addSavedAttack: (attack: Attack) => void;
  updateSavedAttack: (attack: Attack) => void;
  removeSavedAttack: (attackId: string) => void;
}

export type ClientStoreState = SavedAttacksState;

export const useClientStore = create<ClientStoreState>()(
  devtools(
    (set) => ({
      savedAttacks: [],

      setSavedAttacks: (attacks: Attack[]) => set({ savedAttacks: attacks }),

      addSavedAttack: (attack: Attack) =>
        set((state) => ({ savedAttacks: [...state.savedAttacks, attack] })),

      updateSavedAttack: (attack: Attack) =>
        set((state) => ({
          savedAttacks: state.savedAttacks.map((a) =>
            a.attackId === attack.attackId ? attack : a
          ),
        })),

      removeSavedAttack: (attackId: string) =>
        set((state) => ({
          savedAttacks: state.savedAttacks.filter(
            (a) => a.attackId !== attackId
          ),
        })),
    }),
    { name: "client-store" }
  )
);

// what store wrould look like without persistance
// interface ClientStoreState {
//   savedAttacks: Attack[] | null;
//   setSavedAttacks: (attacks: Attack[]) => void;
// }

// export const useClientStore = create<ClientStoreState>((set) => ({
//   savedAttacks: null, // Initial state is null

//   // Function to update the savedAttacks state
//   setSavedAttacks: (attacks: Attack[]) => set({ savedAttacks: attacks }),
// }));

// interface SavedAttacksState {
//     savedAttacks: Attack[];
//     setSavedAttacks: (attacks: Attack[]) => void;
//     addSavedAttack: (attack: Attack) => void;
//     updateSavedAttack: (attack: Attack) => void;
//     removeSavedAttack: (attackId: string) => void;
//   }

// interface ClientStoreState {
//   //   savedAttacks: Attack[] | null;
//   //   setSavedAttacks: (attacks: Attack[]) => void;
// }
