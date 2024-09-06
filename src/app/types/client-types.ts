//update this to support new Feeder data structure
export type FeederMessage = {
  id_: string;
  input: number[];
  prediction: number;
};

export type NeuralNetwork = {
  id_: string;
  input: number[];
  prediction: number;
};
