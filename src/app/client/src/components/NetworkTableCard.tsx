import { useState, useMemo } from "react";
import {
  Table,
  TableBody,
  TableCaption,
  TableCell,
  TableFooter,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Switch } from "@/components/ui/switch";
import { Label } from "@/components/ui/label";
import type { FeederMessage } from "../../../types/client-types";
import PcapMetaDataModal from "./PcapMetaDataModal";

const classMap = {
  BENIGN: { value: 0, color: "green" },
  PortScan: { value: 1, color: "yellow" },
  "FTP-Patator": { value: 2, color: "yellow" },
  "SSH-Patator": { value: 3, color: "yellow" },
  "DoS slowloris": { value: 4, color: "orange" },
  "DoS Slowhttptest": { value: 5, color: "orange" },
  "DoS GoldenEye": { value: 6, color: "orange" },
  "DoS Hulk": { value: 7, color: "orange" },
  Bot: { value: 9, color: "red" },
  Heartbleed: { value: 8, color: "red" },
  Infiltration: { value: 10, color: "red" },
  DDoS: { value: 11, color: "red" },
};

const invertedClassMap = Object.fromEntries(
  Object.entries(classMap).map(([key, obj]) => [
    obj.value,
    { name: key, color: obj.color },
  ])
);

export const NetworkTable = ({
  data,
}: {
  data: FeederMessage[] | null | undefined;
}) => {
  const [showNewestFirst, setShowNewestFirst] = useState(false);

  const sortedData = useMemo(() => {
    if (!data || data.length === 0) {
      return [];
    }
    return showNewestFirst ? [...data].reverse() : data;
  }, [data, showNewestFirst]);

  if (!data || data.length === 0) {
    return <p>No data available.</p>;
  }

  return (
    <>
      <div className="flex items-center space-x-2 mb-4">
        <Switch
          id="show-newest-first"
          checked={showNewestFirst}
          onCheckedChange={setShowNewestFirst}
        />
        <Label htmlFor="show-newest-first">Show newest first</Label>
      </div>
      <Table>
        <TableCaption>Details of Feeder Messages</TableCaption>
        <TableHeader>
          <TableRow>
            <TableHead>ID</TableHead>
            <TableHead>Flow Data</TableHead>
            <TableHead>Prediction</TableHead>
            <TableHead>Host</TableHead>
            <TableHead>Target</TableHead>
            <TableHead>Port</TableHead>
            <TableHead>Metadata</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {sortedData.map((message) => (
            <TableRow key={message.id_}>
              <TableCell>{message.id_}</TableCell>
              <TableCell>
                {message.flow_data
                  ? `Size: ${message.flow_data.length}, Peak: ${Math.max(...(message.flow_data || []))}`
                  : "N/A"}
              </TableCell>
              <TableCell
                style={{
                  color: invertedClassMap[message.prediction]?.color || "black",
                }}
              >
                {invertedClassMap[message.prediction]?.name || "Unknown"}
              </TableCell>
              <TableCell>{message?.metadata?.Source_IP || "Unknown"}</TableCell>
              <TableCell>
                {message?.metadata?.Destination_IP || "Unknown"}
              </TableCell>
              <TableCell>
                {message?.metadata?.Destination_Port || "Unknown"}
              </TableCell>
              <TableCell>
                <PcapMetaDataModal metadata={message?.metadata} />
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
        <TableFooter>
          <TableRow>
            <TableCell colSpan={7}>Total Messages: {data.length}</TableCell>
          </TableRow>
        </TableFooter>
      </Table>
    </>
  );
};

export const NetworkTableCard = ({
  data,
}: {
  data: FeederMessage[] | null | undefined;
}) => {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Network Data Table</CardTitle>
        <CardContent>
          Detailed information about the feeder messages.
        </CardContent>
      </CardHeader>
      <CardContent>
        <div
          style={{
            height: "40vh",
            width: "100%",
            overflow: "auto",
            msOverflowStyle: "none",
            scrollbarWidth: "none",
          }}
          className="hide-scrollbar"
        >
          <NetworkTable data={data} />
        </div>
      </CardContent>
    </Card>
  );
};

export default NetworkTableCard;
