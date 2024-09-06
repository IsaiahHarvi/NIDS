import * as grpc from "@grpc/grpc-js";
import * as protoLoader from "@grpc/proto-loader";
import { Client } from "@grpc/grpc-js";
import path from "path";

// const PROTO_PATH = path.resolve(__dirname, "../grpc_/services.proto");
// TODO: Fix the path to the proto file to not be hardcoded
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

// Variable to store the running gRPC client
let activeGrpcClient: any = null;

// gRPC Client logic
export function runGrpcClient(
  mode: "feeder" | "offlineFeeder",
  live: boolean
): void {
  const port = mode === "feeder" ? "50053" : "50054";

  // Create the client using the `Component` service within `services`
  const client = new servicesProto.Component(
    `localhost:${port}`,
    grpc.credentials.createInsecure()
  ) as Client & { forward: Function };

  activeGrpcClient = client; // Store the running client globally

  const message = {
    input: [], // Assuming input is an empty float array for now
    health_check: false,
    collection_name: "",
    prediction: -1,
    mongo_id: "",
  };

  const sendRequest = () => {
    if (!activeGrpcClient) {
      console.log("gRPC client stopped");
      return;
    }

    client.forward(message, (error: grpc.ServiceError, response: any) => {
      if (error) {
        console.error("Error:", error);
      } else {
        console.log("Response:", response.flow);
        if (!live) {
          client.close();
          activeGrpcClient = null;
        }
      }

      // Repeat if live is true
      if (live && activeGrpcClient) {
        sendRequest();
      }
    });
  };

  // Initial request
  sendRequest();
}

// Function to stop the gRPC client
export function stopGrpcClient() {
  if (activeGrpcClient) {
    console.log("Stopping the gRPC client...");
    activeGrpcClient.close();
    activeGrpcClient = null;
  } else {
    console.log("No active gRPC client to stop.");
  }
}
