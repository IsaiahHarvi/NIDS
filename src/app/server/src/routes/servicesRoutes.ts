import { nanoid } from "nanoid";
import { Elysia } from "elysia";
import { storeServiceDb } from "../database";
import { runGrpcClient, stopGrpcClient } from "../lib/grpcClient";

export const ServicesRoutes = new Elysia().group("/api/services", (router) =>
  router
    // Get data from NeuralNetwork collection
    .get("/neural_network", async () => {
      return storeServiceDb.collection("NeuralNetwork").find().toArray();
    })

    // Get data from Feeder collection
    .get("/feeder", async () => {
      return storeServiceDb.collection("Feeder").find().toArray();
    })

    // Get data from OfflineFeeder collection
    .get("/offline_feeder", async () => {
      return storeServiceDb.collection("OfflineFeeder").find().toArray();
    })

    // Get data from Default collection
    .get("/default", async () => {
      return storeServiceDb.collection("Default").find().toArray();
    })

    // gRPC routes
    .post("/feeder/start", async () => {
      runGrpcClient("feeder", true); // Call the gRPC client function with feeder mode
      return { message: "gRPC client for Feeder started" };
    })

    // Start gRPC client for OfflineFeeder
    .post("/offline_feeder/start", async () => {
      runGrpcClient("offlineFeeder", true); // Call the gRPC client function with offlineFeeder mode
      return { message: "gRPC client for OfflineFeeder started" };
    })

    // Stop gRPC client
    .post("/feeder/stop", async () => {
      stopGrpcClient();
      return { message: "gRPC client stopped" };
    })

    // Delete a document by id_ from NeuralNetwork collection
    .delete("/neural_network/:id_", async (req) => {
      const { id_ } = req.params;
      await storeServiceDb.collection("NeuralNetwork").deleteOne({ id_ });
      return { id_ };
    })

    // Delete a document by id_ from Feeder collection
    .delete("/feeder/:id_", async (req) => {
      const { id_ } = req.params;
      await storeServiceDb.collection("Feeder").deleteOne({ id_ });
      return { id_ };
    })

    // Delete a document by id_ from OfflineFeeder collection
    .delete("/offline_feeder/:id_", async (req) => {
      const { id_ } = req.params;
      await storeServiceDb.collection("OfflineFeeder").deleteOne({ id_ });
      return { id_ };
    })

    // Delete a document by id_ from Default collection
    .delete("/default/:id_", async (req) => {
      const { id_ } = req.params;
      await storeServiceDb.collection("Default").deleteOne({ id_ });
      return { id_ };
    })

    // Delete all documents from NeuralNetwork collection
    .delete("/neural_network", async () => {
      await storeServiceDb.collection("NeuralNetwork").deleteMany({});
      return {
        message: "All documents from NeuralNetwork have been deleted",
      };
    })

    // Delete all documents from Feeder collection
    .delete("/feeder", async () => {
      await storeServiceDb.collection("Feeder").deleteMany({});
      return { message: "All documents from Feeder have been deleted" };
    })

    // Delete all documents from OfflineFeeder collection
    .delete("/offline_feeder", async () => {
      await storeServiceDb.collection("OfflineFeeder").deleteMany({});
      return {
        message: "All documents from OfflineFeeder have been deleted",
      };
    })

    // Delete all documents from Default collection
    .delete("/default", async () => {
      await storeServiceDb.collection("Default").deleteMany({});
      return { message: "All documents from Default have been deleted" };
    })
);
