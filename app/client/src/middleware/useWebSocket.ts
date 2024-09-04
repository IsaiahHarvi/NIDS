import { useContext } from "react";
import { WebSocketContext } from "@/middleware/WebSocketContext";
export const useWebSocket = () => useContext(WebSocketContext);
