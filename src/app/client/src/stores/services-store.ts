import create from "zustand";
import { devtools } from "zustand/middleware";
import { persist } from "zustand/middleware";
import { sendReports } from "@/middleware/api/functions/sendReports";

interface Feeder {
  id_: string;
  flow_data: number[];
  prediction: number;
  metadata: Record<string, string>;
}

interface NeuralNetwork {
  id_: string;
  input: number[];
  prediction: number;
}

interface OfflineFeeder {
  id_: string;
  flow_data: number[];
  prediction: number;
  metadata: Record<string, string>;
}

interface Default {
  id_: string;
  input: number[];
  prediction: number;
}

interface FeederState {
  feeders: Feeder[];
  setFeeders: (feeders: Feeder[]) => void;
  addFeeder: (feeder: Feeder) => void;
  updateFeeder: (feeder: Feeder) => void;
  removeFeeder: (feederId: string) => void;
}

interface NeuralNetworkState {
  neuralNetworks: NeuralNetwork[];
  setNeuralNetworks: (neuralNetworks: NeuralNetwork[]) => void;
  addNeuralNetwork: (neuralNetwork: NeuralNetwork) => void;
  updateNeuralNetwork: (neuralNetwork: NeuralNetwork) => void;
  removeNeuralNetwork: (neuralNetworkId: string) => void;
}

interface OfflineFeederState {
  offlineFeeders: OfflineFeeder[];
  setOfflineFeeders: (offlineFeeders: OfflineFeeder[]) => void;
  addOfflineFeeder: (offlineFeeder: OfflineFeeder) => void;
  updateOfflineFeeder: (offlineFeeder: OfflineFeeder) => void;
  removeOfflineFeeder: (offlineFeederId: string) => void;
}

interface DefaultState {
  defaults: Default[];
  setDefaults: (defaults: Default[]) => void;
  addDefault: (defaultDoc: Default) => void;
  updateDefault: (defaultDoc: Default) => void;
  removeDefault: (defaultId: string) => void;
}

export type ServicesState = FeederState &
  NeuralNetworkState &
  OfflineFeederState &
  DefaultState;

export const useServicesStore = create<ServicesState>()(
  persist(
    devtools(
      (set) => ({
        feeders: [],
        setFeeders: (feeders: Feeder[]) => set({ feeders }),
        // addFeeder: (feeder: Feeder) =>
        //   set((state) => ({ feeders: [...state.feeders, feeder] })),

        addFeeder: async (feeder: Feeder) =>
          set((state) => {
            if (state.feeders.length >= 100) {
              sendReports("feeder", state.feeders);
              return { feeders: [] };
            }
            return {
              feeders: [...state.feeders, feeder],
            };
          }),
        updateFeeder: (feeder: Feeder) =>
          set((state) => ({
            feeders: state.feeders.map((f) =>
              f.id_ === feeder.id_ ? feeder : f
            ),
          })),

        removeFeeder: (feederId: string) =>
          set((state) => ({
            feeders: state.feeders.filter((f) => f.id_ !== feederId),
          })),

        neuralNetworks: [],

        setNeuralNetworks: (neuralNetworks: NeuralNetwork[]) =>
          set({ neuralNetworks }),

        addNeuralNetwork: (neuralNetwork: NeuralNetwork) =>
          set((state) => ({
            neuralNetworks: [...state.neuralNetworks, neuralNetwork],
          })),

        updateNeuralNetwork: (neuralNetwork: NeuralNetwork) =>
          set((state) => ({
            neuralNetworks: state.neuralNetworks.map((n) =>
              n.id_ === neuralNetwork.id_ ? neuralNetwork : n
            ),
          })),

        removeNeuralNetwork: (neuralNetworkId: string) =>
          set((state) => ({
            neuralNetworks: state.neuralNetworks.filter(
              (n) => n.id_ !== neuralNetworkId
            ),
          })),

        offlineFeeders: [],

        setOfflineFeeders: (offlineFeeders: OfflineFeeder[]) =>
          set({ offlineFeeders }),

        addOfflineFeeder: async (offlineFeeder: OfflineFeeder) =>
          set((state) => {
            if (state.offlineFeeders.length >= 100) {
              sendReports("offline_feeder", state.offlineFeeders);
              return { offlineFeeders: [] };
            }
            return {
              offlineFeeders: [...state.offlineFeeders, offlineFeeder],
            };
          }),

        updateOfflineFeeder: (offlineFeeder: OfflineFeeder) =>
          set((state) => ({
            offlineFeeders: state.offlineFeeders.map((o) =>
              o.id_ === offlineFeeder.id_ ? offlineFeeder : o
            ),
          })),

        removeOfflineFeeder: (offlineFeederId: string) =>
          set((state) => ({
            offlineFeeders: state.offlineFeeders.filter(
              (o) => o.id_ !== offlineFeederId
            ),
          })),

        defaults: [],

        setDefaults: (defaults: Default[]) => set({ defaults }),

        addDefault: (defaultDoc: Default) =>
          set((state) => ({ defaults: [...state.defaults, defaultDoc] })),

        updateDefault: (defaultDoc: Default) =>
          set((state) => ({
            defaults: state.defaults.map((d) =>
              d.id_ === defaultDoc.id_ ? defaultDoc : d
            ),
          })),

        removeDefault: (defaultId: string) =>
          set((state) => ({
            defaults: state.defaults.filter((d) => d.id_ !== defaultId),
          })),
      }),
      { name: "services-store" }
    ),
    { name: "services-store" }
  )
);
