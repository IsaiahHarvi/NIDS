import { restGet } from "../../rest-calls/rest-get";
import { FeederMessage } from "../../../../../types/client-types";

export async function getOfflineFeeders(): Promise<FeederMessage[]> {
  try {
    const fetchedData = await restGet("/services/offline_feeder");
    console.log(fetchedData);
    return fetchedData as FeederMessage[];
  } catch (error) {
    console.error("Error fetching offline feeder data:", error);
    return [] as FeederMessage[];
  }
}
