import { ServicesState as services_store_state } from "@/stores/services-store";

export async function handleFeeder(
  data: string,
  store: services_store_state,
  type: string
) {
  const { addFeeder, removeFeeder } = store;
  console.log(
    `Feeder ${type === "feeder_insert" ? "Inserted" : "Deleted"}: `,
    data
  );
  if (data === undefined) return;
  const parsedData = JSON.parse(data);

  if (type === "feeder_insert") {
    addFeeder(parsedData.document);
  } else if (type === "feeder_delete") {
    removeFeeder(parsedData.document);
  }
}

export async function handleNeuralNetwork(
  data: string,
  store: services_store_state,
  type: string
) {
  const { addNeuralNetwork, removeNeuralNetwork } = store;
  console.log(
    `Neural Network ${type === "neural_network_insert" ? "Inserted" : "Deleted"}: `,
    data
  );
  if (data === undefined) return;
  const parsedData = JSON.parse(data);

  if (type === "neural_network_insert") {
    addNeuralNetwork(parsedData.document);
  } else if (type === "neural_network_delete") {
    removeNeuralNetwork(parsedData.document);
  }
}

export async function handleOfflineFeeder(
  data: string,
  store: services_store_state,
  type: string
) {
  const { addOfflineFeeder, removeOfflineFeeder } = store;
  console.log(
    `Offline Feeder ${type === "offline_feeder_insert" ? "Inserted" : "Deleted"}: `,
    data
  );
  if (data === undefined) return;
  const parsedData = JSON.parse(data);

  if (type === "offline_feeder_insert") {
    addOfflineFeeder(parsedData.document);
  } else if (type === "offline_feeder_delete") {
    removeOfflineFeeder(parsedData.document);
  }
}

export async function handleDefault(
  data: string,
  store: services_store_state,
  type: string
) {
  const { addDefault, removeDefault } = store;
  console.log(
    `Default ${type === "default_insert" ? "Inserted" : "Deleted"}: `,
    data
  );
  if (data === undefined) return;
  const parsedData = JSON.parse(data);

  if (type === "default_insert") {
    addDefault(parsedData.document);
  } else if (type === "default_delete") {
    removeDefault(parsedData.document);
  }
}
