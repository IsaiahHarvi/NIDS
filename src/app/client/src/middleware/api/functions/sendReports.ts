import { restPost } from "../../rest-calls/rest-post";
import { FeederMessage } from "../../../../../types/client-types";

export async function sendReports(
  clientType: "feeder" | "offline_feeder",
  feederState: FeederMessage[]
) {
  try {
    const postReport = await restPost(
      `/services/${clientType}Reports`,
      JSON.stringify(feederState)
    );
    return postReport;
  } catch (error) {
    console.error(`Error starting gRPC client for ${clientType}:`, error);
    throw new Error(`Failed to start gRPC client for ${clientType}`);
  }
}
