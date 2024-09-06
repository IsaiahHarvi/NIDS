export type Attack = {
  attackId: string; // Unique identifier for the attack
  name: string; // Name of the attack
  description: string; // Detailed description of the attack
  severity: "low" | "medium" | "high"; // Severity level of the attack
  sourceIp: string; // IP address of the attacker
  destinationIp: string; // IP address of the target
  protocol: "TCP" | "UDP" | "ICMP" | "Other"; // Network protocol used in the attack
  startTime: Date; // Start time of the attack
  endTime?: Date; // Optional end time of the attack
  detected: boolean; // Whether the attack has been detected
  mitigationActions: string[]; // List of mitigation actions taken
};
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
