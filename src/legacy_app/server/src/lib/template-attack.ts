import { nanoid } from "nanoid";
import { Attack } from "../../../types/client-types";

const templateAttack: Attack = {
  attackId: nanoid(),
  name: "SQL Injection",
  description:
    "An SQL injection attack where malicious SQL queries are inserted into input fields.",
  severity: "high",
  sourceIp: "192.168.1.100",
  destinationIp: "192.168.1.10",
  protocol: "TCP",
  startTime: new Date("2024-08-28T10:00:00Z"),
  detected: true,
  mitigationActions: [
    "Blocked IP address 192.168.1.100",
    "Reset database connection",
    "Logged incident for further analysis",
  ],
};

export { templateAttack };
