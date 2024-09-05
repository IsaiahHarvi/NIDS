import { z } from "zod";
import type { WebSocketMessage } from "../../../../types/websocket-types";

export const WebSocketSchema: z.ZodType<WebSocketMessage> = z.object({
  id: z.string().optional(),
  type: z.string().optional(),
  payload: z.object({}).catchall(z.any()).optional(),
});
