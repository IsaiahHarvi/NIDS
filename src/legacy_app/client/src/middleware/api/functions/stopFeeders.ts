import { restPost } from "../../rest-calls/rest-post";

export async function stopFeeders() {
  try {
    const postResponse = await restPost(`/services/feeder/stop`, "");
    console.log(`gRPC client for feeders stopping:`, postResponse);
    return postResponse;
  } catch (error) {
    console.error(`Error stopping gRPC client for feeders:`, error);
    throw new Error(`Failed to start gRPC client for feeders`);
  }
}
