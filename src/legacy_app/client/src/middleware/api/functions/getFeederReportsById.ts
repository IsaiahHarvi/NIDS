import { restGet } from "../../rest-calls/rest-get";
import { FeederMessage } from "../../../../../types/client-types";

// interface FeederReports

export async function getFeederReportById(
  id: string
): Promise<{ id_: string } | null> {
  try {
    const fetchedData = await restGet(`/services/feederReports/${id}`);
    return fetchedData as FeederMessage;
  } catch (error) {
    console.error(`Error fetching offline feeder report with id ${id}:`, error);
    return null; // Return null if the request fails
  }
}
