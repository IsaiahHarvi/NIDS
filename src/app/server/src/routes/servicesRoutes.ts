import { nanoid } from "nanoid";
import { Elysia } from "elysia";
import { storeServiceDb } from "../database";
export const ServicesRoutes = new Elysia().group("/api/services", (router) =>
  router
    // Get data from NeuralNetwork collection
    .get("/neural_network", async () => {
      console.log("Fetching NeuralNetwork data");
      return storeServiceDb.collection("NeuralNetwork").find().toArray();
    })

    // Get data from Feeder collection
    .get("/feeder", async () => {
      console.log("Fetching Feeder data");
      return storeServiceDb.collection("Feeder").find().toArray();
    })

    // Get data from OfflineFeeder collection
    .get("/offline_feeder", async () => {
      console.log("Fetching OfflineFeeder data");
      return storeServiceDb.collection("OfflineFeeder").find().toArray();
    })

    // Get data from Default collection
    .get("/default", async () => {
      console.log("Fetching Default data");
      return storeServiceDb.collection("Default").find().toArray();
    })

    // Delete a document by id_ from NeuralNetwork collection
    .delete("/neural_network/:id_", async (req) => {
      const { id_ } = req.params;
      console.log(`Deleting document with id_ ${id_} from NeuralNetwork`);
      await storeServiceDb.collection("NeuralNetwork").deleteOne({ id_ });
      return { id_ };
    })

    // Delete a document by id_ from Feeder collection
    .delete("/feeder/:id_", async (req) => {
      const { id_ } = req.params;
      console.log(`Deleting document with id_ ${id_} from Feeder`);
      await storeServiceDb.collection("Feeder").deleteOne({ id_ });
      return { id_ };
    })

    // Delete a document by id_ from OfflineFeeder collection
    .delete("/offline_feeder/:id_", async (req) => {
      const { id_ } = req.params;
      console.log(`Deleting document with id_ ${id_} from OfflineFeeder`);
      await storeServiceDb.collection("OfflineFeeder").deleteOne({ id_ });
      return { id_ };
    })

    // Delete a document by id_ from Default collection
    .delete("/default/:id_", async (req) => {
      const { id_ } = req.params;
      console.log(`Deleting document with id_ ${id_} from Default`);
      await storeServiceDb.collection("Default").deleteOne({ id_ });
      return { id_ };
    })

    // Delete all documents from NeuralNetwork collection
    .delete("/neural_network", async () => {
      console.log("Deleting all documents from NeuralNetwork");
      await storeServiceDb.collection("NeuralNetwork").deleteMany({});
      return {
        message: "All documents from NeuralNetwork have been deleted",
      };
    })

    // Delete all documents from Feeder collection
    .delete("/feeder", async () => {
      console.log("Deleting all documents from Feeder");
      await storeServiceDb.collection("Feeder").deleteMany({});
      return { message: "All documents from Feeder have been deleted" };
    })

    // Delete all documents from OfflineFeeder collection
    .delete("/offline_feeder", async () => {
      console.log("Deleting all documents from OfflineFeeder");
      await storeServiceDb.collection("OfflineFeeder").deleteMany({});
      return {
        message: "All documents from OfflineFeeder have been deleted",
      };
    })

    // Delete all documents from Default collection
    .delete("/default", async () => {
      console.log("Deleting all documents from Default");
      await storeServiceDb.collection("Default").deleteMany({});
      return { message: "All documents from Default have been deleted" };
    })
);
