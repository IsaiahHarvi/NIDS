//update this to support new Feeder data structure
export type FeederMessage = {
  id_: string;
  flow_data: number[];
  prediction: number;
  metadata: Record<string, string>;
};

export type NeuralNetwork = {
  id_: string;
  input: number[];
  prediction: number;
};
