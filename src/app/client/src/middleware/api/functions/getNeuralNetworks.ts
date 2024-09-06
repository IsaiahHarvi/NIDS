import { restGet } from "../../rest-calls/rest-get";
import { NeuralNetwork } from "../../../../../types/client-types";

export async function getNeuralNetworks(): Promise<NeuralNetwork[]> {
  try {
    const fetchedData = await restGet("/services/neural_network");
    console.log(fetchedData);
    return fetchedData as NeuralNetwork[];
  } catch (error) {
    console.error("Error fetching Neural Network data:", error);
    return [] as NeuralNetwork[];
  }
}
