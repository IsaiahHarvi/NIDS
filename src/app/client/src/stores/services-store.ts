import create from "zustand";
import { devtools } from "zustand/middleware";
// import { persist } from "zustand/middleware";

// Define the types for your collections
interface Feeder {
  id_: string;
  input: number[];
  prediction: number;
}

interface NeuralNetwork {
  id_: string;
  input: number[];
  prediction: number;
}

interface OfflineFeeder {
  id_: string;
  input: number[];
  prediction: number;
}

interface Default {
  id_: string;
  input: number[];
  prediction: number;
}

// Define the state interfaces for each collection
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
  devtools(
    (set) => ({
      // Feeder collection state and actions
      feeders: [],

      setFeeders: (feeders: Feeder[]) => set({ feeders }),

      addFeeder: (feeder: Feeder) =>
        set((state) => ({ feeders: [...state.feeders, feeder] })),

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

      // NeuralNetwork collection state and actions
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

      // OfflineFeeder collection state and actions
      offlineFeeders: [],

      setOfflineFeeders: (offlineFeeders: OfflineFeeder[]) =>
        set({ offlineFeeders }),

      addOfflineFeeder: (offlineFeeder: OfflineFeeder) =>
        set((state) => ({
          offlineFeeders: [...state.offlineFeeders, offlineFeeder],
        })),

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

      // Default collection state and actions
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
  )
);
