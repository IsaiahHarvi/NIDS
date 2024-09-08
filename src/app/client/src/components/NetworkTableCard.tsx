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
import {
  Card,
  CardHeader,
  CardTitle,
  CardContent,
  CardDescription,
} from "@/components/ui/card";
import type { FeederMessage } from "../../../types/client-types";

// Table component for rendering the data
export const NetworkTable = ({ data }: { data: FeederMessage[] }) => {
  return (
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
        {data.map((message) => (
          <TableRow key={message.id_}>
            <TableCell>{message.id_}</TableCell>
            <TableCell>
              {/* Render flow_data array as a string */}
              {message.flow_data?.join(", ") || "N/A"}
            </TableCell>
            <TableCell>{message.prediction}</TableCell>
            <TableCell>{message.metadata.Source_IP}</TableCell>
            <TableCell>{message.metadata.Destination_IP}</TableCell>
            <TableCell>{message.metadata.Destination_Port}</TableCell>
            {/* <TableCell>
              {Object.entries(message.metadata)
                .map(([key, value]) => `${key}: ${value}`)
                .join(", ")}
            </TableCell> */}
          </TableRow>
        ))}
      </TableBody>
      <TableFooter>
        <TableRow>
          <TableCell colSpan={7}>Total Messages: {data.length}</TableCell>
        </TableRow>
      </TableFooter>
    </Table>
  );
};

// Card wrapper component for the NetworkTable
export const NetworkTableCard = ({ data }: { data: FeederMessage[] }) => {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Network Data Table</CardTitle>
        <CardDescription>
          Detailed information about the feeder messages.
        </CardDescription>
      </CardHeader>
      <CardContent>
        {/* Render the NetworkTable without any styling */}
        <div style={{ height: "40vh", width: "80%", overflow: "auto" }}>
          <NetworkTable data={data} />
        </div>
      </CardContent>
    </Card>
  );
};

export default NetworkTableCard;
