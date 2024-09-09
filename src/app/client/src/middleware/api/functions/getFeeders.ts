import { restGet } from "../../rest-calls/rest-get";
import { FeederMessage } from "../../../../../types/client-types";

export async function getFeeders(): Promise<FeederMessage[]> {
  try {
    const fetchedData = await restGet("/services/feeder");
    return fetchedData as FeederMessage[];
  } catch (error) {
    console.error("Error fetching feeder data:", error);
    return [] as FeederMessage[];
  }
}
