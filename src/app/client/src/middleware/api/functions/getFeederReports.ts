import { restGet } from "../../rest-calls/rest-get";
// import { FeederMessage } from "../../../../../types/client-types";

// interface FeederReports

export async function getFeederReports(): Promise<
  { timestamp: string; id: string }[]
> {
  try {
    const fetchedData = await restGet("/services/feederReports");
    return fetchedData as { timestamp: string; id: string }[];
  } catch (error) {
    console.error("Error fetching feeder data:", error);
    return [];
  }
}
