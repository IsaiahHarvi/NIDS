import { storeServiceDb } from "../database";
import { Stream } from "@elysiajs/stream";
import { ElysiaWS } from "elysia/dist/ws";

export function storeServicesChangeStream(ws: ElysiaWS<any, any, any>) {
  return new Stream((stream) => {
    const feederChangeStream = storeServiceDb
      ?.collection("Feeder")
      .watch([], { fullDocument: "updateLookup", showExpandedEvents: true });

    const neuralNetworkChangeStream = storeServiceDb
      ?.collection("NeuralNetwork")
      .watch([], { fullDocument: "updateLookup", showExpandedEvents: true });

    const offlineFeederChangeStream = storeServiceDb
      ?.collection("OfflineFeeder")
      .watch([], { fullDocument: "updateLookup", showExpandedEvents: true });

    const defaultChangeStream = storeServiceDb.watch([], {
      fullDocument: "updateLookup",
      showExpandedEvents: true,
    });

    // Feeder collection on change
    feederChangeStream.on("change", async (next) => {
      if (next.operationType === "insert") {
        const cleanedData = { ...next.fullDocument };
        delete cleanedData._id;

        ws.send({
          type: "feeder_insert",
          payload: {
            collection: next.ns.coll,
            document: cleanedData,
          },
        });
      }
      if (next.operationType === "delete") {
        ws.send({
          type: "feeder_delete",
          payload: {
            collection: next.ns.coll,
            document: next.documentKey,
          },
        });
      }
    });

    feederChangeStream.on("error", (error) => {
      console.log("Error in feederChangeStream: ", error);
      stream.send({ error: error.message });
      stream.close();
    });

    // NeuralNetwork collection on change
    neuralNetworkChangeStream.on("change", async (next) => {
      if (next.operationType === "insert") {
        const cleanedData = { ...next.fullDocument };
        delete cleanedData._id;

        ws.send({
          type: "neural_network_insert",
          payload: {
            collection: next.ns.coll,
            document: cleanedData,
          },
        });
      }
      if (next.operationType === "delete") {
        ws.send({
          type: "neural_network_delete",
          payload: {
            collection: next.ns.coll,
            document: next.documentKey,
          },
        });
      }
    });

    neuralNetworkChangeStream.on("error", (error) => {
      console.log("Error in neuralNetworkChangeStream: ", error);
      stream.send({ error: error.message });
      stream.close();
    });

    // OfflineFeeder collection on change
    offlineFeederChangeStream.on("change", async (next) => {
      if (next.operationType === "insert") {
        const cleanedData = { ...next.fullDocument };
        delete cleanedData._id;

        ws.send({
          type: "offline_feeder_insert",
          payload: {
            collection: next.ns.coll,
            document: cleanedData,
          },
        });
      }
      if (next.operationType === "delete") {
        ws.send({
          type: "offline_feeder_delete",
          payload: {
            collection: next.ns.coll,
            document: next.documentKey,
          },
        });
      }
    });

    offlineFeederChangeStream.on("error", (error) => {
      console.log("Error in offlineFeederChangeStream: ", error);
      stream.send({ error: error.message });
      stream.close();
    });

    // Default collection on change
    defaultChangeStream.on("change", async (next) => {
      if (next.operationType === "insert") {
        const cleanedData = { ...next.fullDocument };
        delete cleanedData._id;

        ws.send({
          type: "default_insert",
          payload: {
            collection: next.ns.coll,
            document: cleanedData,
          },
        });
      }
      if (next.operationType === "delete") {
        ws.send({
          type: "default_delete",
          payload: {
            collection: next.ns.coll,
            document: next.documentKey,
          },
        });
      }
    });

    defaultChangeStream.on("error", (error) => {
      console.log("Error in defaultChangeStream: ", error);
      stream.send({ error: error.message });
      stream.close();
    });
  });
}
