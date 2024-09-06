import { createContext, useEffect } from "react";
import useWebSocket from "react-use-websocket";
import { useServicesStore } from "@/stores/services-store";
import { WebSocketSchema } from "@/lib/zod-schemas/websocket-schemas";
import type {
  Wrapper,
  WebSocketContextProps,
} from "../../../types/websocket-types";
import {
  handleFeeder,
  handleNeuralNetwork,
  handleOfflineFeeder,
  handleDefault,
} from "@/lib/websocket-utils";

export const WebSocketContext = createContext<WebSocketContextProps>(
  {} as WebSocketContextProps
);

export default function WebSocketContextProvider({ children }: Wrapper) {
  const services_store = useServicesStore();
  const url = "ws://localhost:8000/api/ws";

  const { sendMessage, lastJsonMessage } = useWebSocket(url, {
    onOpen: () => {
      sendMessage("Hello From Client");
    },
    onError: (e) => console.log("WebSocket error: ", e),
  });

  useEffect(() => {
    try {
      if (lastJsonMessage === null) return;
      const message = WebSocketSchema.parse(lastJsonMessage); // Parse will throw for invalid events
      if (message.type === undefined) return;
      switch (message.type) {
        case "feeder_insert":
        case "feeder_delete":
          console.log(`${message.type} message: `, message.payload);
          handleFeeder(
            JSON.stringify(message.payload),
            services_store,
            message.type
          );
          break;
        case "neural_network_insert":
        case "neural_network_delete":
          console.log(`${message.type} message: `, message.payload);
          handleNeuralNetwork(
            JSON.stringify(message.payload),
            services_store,
            message.type
          );
          break;
        case "offline_feeder_insert":
        case "offline_feeder_delete":
          console.log(`${message.type} message: `, message.payload);
          handleOfflineFeeder(
            JSON.stringify(message.payload),
            services_store,
            message.type
          );
          break;
        case "default_insert":
        case "default_delete":
          console.log(`${message.type} message: `, message.payload);
          handleDefault(
            JSON.stringify(message.payload),
            services_store,
            message.type
          );
          break;
      }
    } catch (error) {
      console.log("Error in handleJsonMessage: ", error);
    }
  }, [lastJsonMessage]);

  // const updateConnectionStatus = (rs: string) => {
  //   client_store.setConnectionStatus(rs);
  // };

  // const connectionStatus = {
  //   [ReadyState.CONNECTING]: "Connecting",
  //   [ReadyState.OPEN]: "Open",
  //   [ReadyState.CLOSING]: "Closing",
  //   [ReadyState.CLOSED]: "Closed",
  //   [ReadyState.UNINSTANTIATED]: "Uninstantiated",
  // }[readyState];

  // useEffect(() => {
  //   // console.log("WebSocket connection status: ", connectionStatus);
  //   updateConnectionStatus(connectionStatus);
  // }, [readyState]);

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
