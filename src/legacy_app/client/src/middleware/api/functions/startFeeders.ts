import { restPost } from "../../rest-calls/rest-post";

export async function startFeeders(clientType: "feeder" | "offline_feeder") {
  try {
    const postResponse = await restPost(`/services/${clientType}/start`, "");
    console.log(`gRPC client for ${clientType} started:`, postResponse);
    return postResponse;
  } catch (error) {
    console.error(`Error starting gRPC client for ${clientType}:`, error);
    throw new Error(`Failed to start gRPC client for ${clientType}`);
  }
}
