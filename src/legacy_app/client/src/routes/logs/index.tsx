"use client";

import { useState } from "react";
import { createFileRoute } from "@tanstack/react-router";
import { Card, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { ScrollArea } from "@/components/ui/scroll-area";

// Mock data for logs
const mockLogs = [
  {
    _id: "6732ab9b49d87b12192868ea",
    id_: "76061bc7-5ed2-4c1f-bafd-1cb02c47e759",
    prediction: 0,
    metadata: {
      Source_IP: "192.168.10.5",
      Destination_IP: "91.215.100.40",
      Protocol: 6,
      Label: "BENIGN",
    },
  },
  {
    _id: "6732ab9b49d87b12192868eb",
    id_: "8f061bc7-5ed2-4c1f-bafd-1cb02c47e760",
    prediction: 1,
    metadata: {
      Source_IP: "10.0.0.1",
      Destination_IP: "203.0.113.0",
      Protocol: 17,
      Label: "MALICIOUS",
    },
  },
  {
    _id: "6732ab9b49d87b12192868ec",
    id_: "9a061bc7-5ed2-4c1f-bafd-1cb02c47e761",
    prediction: 0,
    metadata: {
      Source_IP: "172.16.0.1",
      Destination_IP: "8.8.8.8",
      Protocol: 6,
      Label: "BENIGN",
    },
  },
];

export const Route = createFileRoute("/logs/")({
  component: LogTerminal,
});

function LogTerminal() {
  const [filter, setFilter] = useState("");

  const filteredLogs = mockLogs.filter(
    (log) =>
      log._id.includes(filter) ||
      log.id_.includes(filter) ||
      log.metadata.Source_IP.includes(filter) ||
      log.metadata.Destination_IP.includes(filter) ||
      log.metadata.Label.includes(filter)
  );

  return (
    <div className="p-8">
      <Card className="border-2">
        <CardContent className="p-6">
          <div className="mb-4">
            <h2 className="text-white text-xl mb-4">Logs</h2>
            <Input
              type="text"
              placeholder="Filter logs..."
              value={filter}
              onChange={(e) => setFilter(e.target.value)}
              className=" "
            />
          </div>
          <ScrollArea className="h-[600px] w-full rounded-md border p-4">
            <div className="font-mono text-sm space-y-6">
              {filteredLogs.map((log, index) => (
                <div key={log._id} className="">
                  {`Log ${index + 1}:`}
                  <br />
                  {`ID: ${log._id}`}
                  <br />
                  {`UUID: ${log.id_}`}
                  <br />
                  {`Prediction: ${log.prediction}`}
                  <br />
                  {`Source IP: ${log.metadata.Source_IP}`}
                  <br />
                  {`Destination IP: ${log.metadata.Destination_IP}`}
                  <br />
                  {`Protocol: ${log.metadata.Protocol}`}
                  <br />
                  {`Label: ${log.metadata.Label}`}
                </div>
              ))}
            </div>
          </ScrollArea>
        </CardContent>
      </Card>
    </div>
  );
}
