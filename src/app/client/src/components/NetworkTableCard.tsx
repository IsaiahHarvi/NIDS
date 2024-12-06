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
  benign: { value: 0, color: "green" },
  malicious: { value: 1, color: "red" },
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
            <TableHead>Source IP</TableHead>
            <TableHead>Destination IP</TableHead>
            <TableHead>Ports</TableHead>
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
              <TableCell>{message?.metadata?.src_ip || "Unknown"}</TableCell>
              <TableCell>{message?.metadata?.dst_ip || "Unknown"}</TableCell>
              <TableCell>
                Src: {message?.metadata?.src_port || "N/A"}, Dst:{" "}
                {message?.metadata?.dst_port || "N/A"}
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
