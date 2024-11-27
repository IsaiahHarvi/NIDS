import { restGet } from "../../rest-calls/rest-get";
// import { FeederMessage } from "../../../../../types/client-types";

// interface FeederReports

export async function getOfflineFeederReportById(
  id: string
): Promise<{ id_: string } | null> {
  try {
    const fetchedData = await restGet(`/services/offline_feederReports/${id}`);
    return fetchedData as { id_: string };
  } catch (error) {
    console.error(`Error fetching offline feeder report with id ${id}:`, error);
    return null; // Return null if the request fails
  }
}
