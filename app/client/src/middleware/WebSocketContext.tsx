import { createContext, useEffect } from "react";
import useWebSocket from "react-use-websocket";
import { useServicesStore } from "@/stores/services-store";
import { WebSocketSchema } from "@/lib/zod-schemas/websocket-schemas";
import type {
  Wrapper,
  WebSocketContextProps,
} from "../../../types/websocket-types";
import {
  handleFeederInsert,
  handleFeederDelete,
  handleNeuralNetworkInsert,
  handleNeuralNetworkDelete,
  handleOfflineFeederInsert,
  handleOfflineFeederDelete,
  handleDefaultInsert,
  handleDefaultDelete,
} from "@/lib/websocket-utils";

export const WebSocketContext = createContext<WebSocketContextProps>(
  {} as WebSocketContextProps
);

export default function WebSocketContextProvider({ children }: Wrapper) {
  const services_store = useServicesStore();
  const url = "ws://localhost:3000/api/ws";

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
        case "pong":
          break;
        case "test":
          break;
        case "current_attack_insert":
          if (message.payload === undefined) return;
          // handleCurrentAttackInsert(JSON.stringify(message.payload), client_store);
          break;
        case "current_attack_delete":
          break;
        case "feeder_insert":
          console.log("feeder_insert message: ", message.payload);
          handleFeederInsert(JSON.stringify(message.payload), services_store);
          break;
        case "feeder_delete":
          console.log("feeder_delete message: ", message.payload);
          handleFeederDelete(JSON.stringify(message.payload), services_store);
          break;
        case "neural_network_insert":
          console.log("neural_network_insert message: ", message.payload);
          handleNeuralNetworkInsert(
            JSON.stringify(message.payload),
            services_store
          );
          break;
        case "neural_network_delete":
          console.log("neural_network_delete message: ", message.payload);
          handleNeuralNetworkDelete(
            JSON.stringify(message.payload),
            services_store
          );
          break;
        case "offline_feeder_insert":
          console.log("offline_feeder_insert message: ", message.payload);
          handleOfflineFeederInsert(
            JSON.stringify(message.payload),
            services_store
          );
          break;
        case "offline_feeder_delete":
          console.log("offline_feeder_delete message: ", message.payload);
          handleOfflineFeederDelete(
            JSON.stringify(message.payload),
            services_store
          );
          break;
        case "default_insert":
          console.log("default_insert message: ", message.payload);
          handleDefaultInsert(JSON.stringify(message.payload), services_store);
          break;
        case "default_delete":
          console.log("default_delete message: ", message.payload);
          handleDefaultDelete(JSON.stringify(message.payload), services_store);
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
