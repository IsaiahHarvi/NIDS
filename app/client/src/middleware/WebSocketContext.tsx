// import {
//   handleTcaiStatusData,
//   handleLoggerComponentsData,
// } from "@/lib/websocket-utils";
// import { handleVSUTData } from "@/middleware/websocket-utils/vsut-handlers";
import { createContext, useEffect } from "react";
import useWebSocket from "react-use-websocket";
import { ReadyState } from "react-use-websocket";
// import { useVsutStore } from "./stores/vsut-store";
// import { useClientStore } from "./stores/client-store";
import { useClientStore } from "@/stores/client-store";
// import { useTcaiLogsStore } from "./stores/tcai-logs-store";
// import { useLoggerComponentsStore } from "./stores/logger-components-store";
// import { useTransientPulseStore } from "./stores/transient-pulse-store";
import { WebSocketSchema } from "@/lib/zod-schemas/websocket-schemas";
import type {
  Wrapper,
  WebSocketContextProps,
} from "../../../types/websocket-types";

export const WebSocketContext = createContext<WebSocketContextProps>(
  {} as WebSocketContextProps
);

export default function WebSocketContextProvider({ children }: Wrapper) {
  const client_store = useClientStore();
  const url = "ws://localhost:3000/api /ws";

  const { sendMessage, lastJsonMessage, readyState } = useWebSocket(url, {
    onOpen: () => {
      sendMessage("Hello From Client");
    },
    onError: (e) => console.log("WebSocket error: ", e),
    heartbeat: {
      message: "ping",
    },
  });

  useEffect(() => {
    try {
      if (lastJsonMessage === null) return;
      const message = WebSocketSchema.parse(lastJsonMessage); // Parse will throw for invalid events
      if (message.type === undefined) return;
      switch (message.type) {
        case "pong":
          // console.log("Received pong message.");
          break;
        case "test":
          // console.log("Received test message.");
          break;
        case "tcai_logs":
          // console.log("Received tcai logs: ", message.payload);
          if (message.payload === undefined) return;
          handleTcaiStatusData(JSON.stringify(message.payload), tcai_store);
          break;
        case "logger_component":
          // console.log("Received logger component data: ", message.payload);
          handleLoggerComponentsData(
            JSON.stringify(message.payload),
            logger_store
          );
          break;
      }
    } catch (error) {
      console.log("Error in handleJsonMessage: ", error);
    }
  }, [lastJsonMessage]);

  const updateConnectionStatus = (rs: string) => {
    client_store.setConnectionStatus(rs);
  };

  const connectionStatus = {
    [ReadyState.CONNECTING]: "Connecting",
    [ReadyState.OPEN]: "Open",
    [ReadyState.CLOSING]: "Closing",
    [ReadyState.CLOSED]: "Closed",
    [ReadyState.UNINSTANTIATED]: "Uninstantiated",
  }[readyState];

  useEffect(() => {
    // console.log("WebSocket connection status: ", connectionStatus);
    updateConnectionStatus(connectionStatus);
  }, [readyState]);

  // this is just an example of how to send a message
  // keeping it so we can use it as a reference if we ever need it
  // const sendMessage = (message: string) => {
  //   sendJsonMessage(JSON.stringify({ message }));
  // };

  return (
    <WebSocketContext.Provider
      value={{
        sendMessage,
      }}
    >
      {children}
    </WebSocketContext.Provider>
  );
}
