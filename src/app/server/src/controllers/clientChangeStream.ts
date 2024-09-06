import { storeServiceDb } from "../database";
import { Stream } from "@elysiajs/stream";
import { ElysiaWS } from "elysia/dist/ws";

export function clientChangeStream(ws: ElysiaWS<any, any, any>) {
  return new Stream((stream) => {
    const currentAttackChangeStream = storeServiceDb
      ?.collection("current_attack")
      .watch([], { fullDocument: "updateLookup", showExpandedEvents: true });

    const savedAttacksChangeStream = storeServiceDb
      ?.collection("saved_attacks")
      .watch([], { fullDocument: "updateLookup", showExpandedEvents: true });

    // current_attack collection on change
    currentAttackChangeStream.on("change", async (next) => {
      if (next.operationType === "insert") {
        const cleanedData = { ...next.fullDocument };
        delete cleanedData._id;

        ws.send({
          type: "current_attack_insert",
          payload: {
            collection: next.ns.coll,
            document: cleanedData,
          },
        });
      }
      if (next.operationType === "delete") {
        ws.send({
          type: "current_attack_delete",
          payload: {
            collection: next.ns.coll,
            document: next.documentKey,
          },
        });
      }
    });

    currentAttackChangeStream.on("error", (error) => {
      console.log("Error in currentAttackChangeStream: ", error);
      stream.send({ error: error.message });
      stream.close();
    });

    // saved_attacks collection on change
    savedAttacksChangeStream.on("change", async (next) => {
      if (next.operationType === "insert") {
        const cleanedData = { ...next.fullDocument };
        delete cleanedData._id;

        ws.send({
          type: "saved_attacks_insert",
          payload: {
            collection: next.ns.coll,
            document: cleanedData,
          },
        });
      }
      if (next.operationType === "delete") {
        ws.send({
          type: "saved_attacks_delete",
          payload: {
            collection: next.ns.coll,
            document: next.documentKey,
          },
        });
      }
    });

    savedAttacksChangeStream.on("error", (error) => {
      console.log("Error in savedAttacksChangeStream: ", error);
      stream.send({ error: error.message });
      stream.close();
    });
  });
}
