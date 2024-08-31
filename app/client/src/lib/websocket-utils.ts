import { ServicesState as services_store_state } from "@/stores/services-store";

// Function to handle inserting feeder data
export async function handleFeederInsert(
  data: string,
  store: services_store_state
) {
  const { addFeeder } = store;
  console.log("Feeder Inserted: ", data);
  if (data === undefined) return;
  const parsedData = JSON.parse(data);
  addFeeder(parsedData.document);
}

// Function to handle deleting feeder data
export async function handleFeederDelete(
  data: string,
  store: services_store_state
) {
  const { removeFeeder } = store;
  console.log("Feeder Deleted: ", data);
  if (data === undefined) return;
  const parsedData = JSON.parse(data);
  removeFeeder(parsedData.document);
}

// Function to handle inserting neural network data
export async function handleNeuralNetworkInsert(
  data: string,
  store: services_store_state
) {
  const { addNeuralNetwork } = store;
  console.log("Neural Network Inserted: ", data);
  if (data === undefined) return;
  const parsedData = JSON.parse(data);
  addNeuralNetwork(parsedData.document);
}

// Function to handle deleting neural network data
export async function handleNeuralNetworkDelete(
  data: string,
  store: services_store_state
) {
  const { removeNeuralNetwork } = store;
  console.log("Neural Network Deleted: ", data);
  if (data === undefined) return;
  const parsedData = JSON.parse(data);
  removeNeuralNetwork(parsedData.document);
}

// Function to handle inserting offline feeder data
export async function handleOfflineFeederInsert(
  data: string,
  store: services_store_state
) {
  const { addOfflineFeeder } = store;
  console.log("Offline Feeder Inserted: ", data);
  if (data === undefined) return;
  const parsedData = JSON.parse(data);
  addOfflineFeeder(parsedData.document);
}

// Function to handle deleting offline feeder data
export async function handleOfflineFeederDelete(
  data: string,
  store: services_store_state
) {
  const { removeOfflineFeeder } = store;
  console.log("Offline Feeder Deleted: ", data);
  if (data === undefined) return;
  const parsedData = JSON.parse(data);
  removeOfflineFeeder(parsedData.document);
}

// Function to handle inserting default data
export async function handleDefaultInsert(
  data: string,
  store: services_store_state
) {
  const { addDefault } = store;
  console.log("Default Inserted: ", data);
  if (data === undefined) return;
  const parsedData = JSON.parse(data);
  addDefault(parsedData.document);
}

// Function to handle deleting default data
export async function handleDefaultDelete(
  data: string,
  store: services_store_state
) {
  const { removeDefault } = store;
  console.log("Default Deleted: ", data);
  if (data === undefined) return;
  const parsedData = JSON.parse(data);
  removeDefault(parsedData.document);
}
