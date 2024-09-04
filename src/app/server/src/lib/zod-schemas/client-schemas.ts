import type { Attack } from "../../../../types/client-types";
import { z } from "zod";

export const AttackSchema: z.ZodSchema<Attack> = z.object({
  attackId: z.string(),
  name: z.string(),
  description: z.string(),
  severity: z.enum(["low", "medium", "high"]),
  sourceIp: z.string(),
  destinationIp: z.string(),
  protocol: z.enum(["TCP", "UDP", "ICMP", "Other"]),
  startTime: z.date(),
  endTime: z.date().optional(),
  detected: z.boolean(),
  mitigationActions: z.array(z.string()),
});
