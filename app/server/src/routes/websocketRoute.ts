import { Elysia } from "elysia";
import { storeServicesChangeStream, clientChangeStream } from "../controllers";

export const websocketRoute = new Elysia().ws("/api/ws", {
  open: (ws) => {
    console.log("WebSocket connection opened.");
    storeServicesChangeStream(ws);
    clientChangeStream(ws);
  },
  close: (ws) => {
    console.log("WebSocket connection closed.");
    ws.close();
  },
  message: (ws, message) => {
    if (message === "ping") {
      ws.send({ type: "pong" });
    }
  },
  sendPings: true,
  pong: () => {
    console.log("WebSocket pong received.");
  },
  ping: () => {
    console.log("WebSocket ping recived.");
  },
});
