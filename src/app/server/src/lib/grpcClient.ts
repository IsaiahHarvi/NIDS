import * as grpc from "@grpc/grpc-js";
import * as protoLoader from "@grpc/proto-loader";
import { Client } from "@grpc/grpc-js";
import path from "path";

const PROTO_PATH = "/workspaces/NIDS/src/grpc_/services.proto";

const packageDefinition = protoLoader.loadSync(PROTO_PATH, {
  keepCase: true,
  longs: String,
  enums: String,
  defaults: true,
  oneofs: true,
});
const protoDescriptor = grpc.loadPackageDefinition(packageDefinition);
const servicesProto = (protoDescriptor as any).services;

let activeGrpcClient: any = null;

function createGrpcClient(mode: "feeder" | "offlineFeeder"): any {
  const port = mode === "feeder" ? "50053" : "50054";
  return new servicesProto.Component(
    `localhost:${port}`,
    grpc.credentials.createInsecure()
  ) as Client & { forward: Function };
}

export function runGrpcClient(
  mode: "feeder" | "offlineFeeder",
  live: boolean
): void {
  const client = createGrpcClient(mode);
  activeGrpcClient = client;

  const message = {
    input: [],
    health_check: false,
    collection_name: "",
    prediction: -1,
    mongo_id: "",
  };

  const sendRequest = (retryCount = 0) => {
    if (!activeGrpcClient) {
      console.log("gRPC client stopped");
      return;
    }

    client.forward(message, (error: grpc.ServiceError, response: any) => {
      if (error) {
        console.error("Error:", error.message);

        if (
          error.code === grpc.status.UNAVAILABLE ||
          error.message.includes("Channel has been shut down")
        ) {
          console.log("Recreating gRPC client...");
          activeGrpcClient = createGrpcClient(mode);

          if (retryCount < 5) {
            const backoffDelay = Math.pow(2, retryCount) * 1000;
            console.log(`Retrying in ${backoffDelay}ms...`);
            setTimeout(() => sendRequest(retryCount + 1), backoffDelay);
          } else {
            console.error("Max retries reached. Stopping client.");
            activeGrpcClient.close();
            activeGrpcClient = null;
          }
        }
        return;
      }

      console.log("Response:", response.flow);

      if (!live) {
        client.close();
        activeGrpcClient = null;
      }

      if (live && activeGrpcClient) {
        sendRequest();
      }
    });
  };

  sendRequest();
}

export function stopGrpcClient() {
  if (activeGrpcClient) {
    console.log("Stopping the gRPC client...");
    activeGrpcClient.close();
    activeGrpcClient = null;
  } else {
    console.log("No active gRPC client to stop.");
  }
}
