import { useMemo } from "react";
import { Pie, PieChart, Label } from "recharts";
import {
  Card,
  CardHeader,
  CardTitle,
  CardContent,
  CardDescription,
} from "@/components/ui/card";
import {
  ChartContainer,
  ChartTooltip,
  ChartTooltipContent,
  ChartConfig,
} from "@/components/ui/chart";
import { FeederMessage } from "../../../types/client-types";

const classMap = {
  BENIGN: { value: 0, color: "green" },
  PortScan: { value: 9, color: "yellow" },
  "FTP-Patator": { value: 7, color: "yellow" },
  "SSH-Patator": { value: 10, color: "yellow" },
  "DoS slowloris": { value: 4, color: "orange" },
  "DoS Slowhttptest": { value: 5, color: "orange" },
  "DoS GoldenEye": { value: 3, color: "orange" },
  "DoS Hulk": { value: 4, color: "orange" },
  Bot: { value: 1, color: "red" },
  Heartbleed: { value: 8, color: "red" },
  // Infiltration: { value: 9, color: "red" },
  DDoS: { value: 2, color: "red" },
};

const invertedClassMap = Object.fromEntries(
  Object.entries(classMap).map(([key, obj]) => [
    obj.value,
    { name: key, color: obj.color },
  ])
);

const PieChartComponent = ({
  data,
}: {
  data: { name: string; value: number; fill: string }[];
}) => {
  const totalOccurrences = useMemo(() => {
    return data.reduce((acc, curr) => acc + curr.value, 0);
  }, [data]);

  return (
    <ChartContainer
      config={chartConfig}
      className="mx-auto aspect-square max-h-[250px]"
    >
      <PieChart>
        <ChartTooltip
          cursor={false}
          content={<ChartTooltipContent hideLabel />}
        />
        <Pie
          data={data}
          dataKey="value"
          nameKey="name"
          innerRadius={60}
          strokeWidth={5}
        >
          <Label
            content={({ viewBox }) => {
              if (viewBox && "cx" in viewBox && "cy" in viewBox) {
                return (
                  <text
                    x={viewBox.cx}
                    y={viewBox.cy}
                    textAnchor="middle"
                    dominantBaseline="middle"
                  >
                    <tspan
                      x={viewBox.cx}
                      y={viewBox.cy}
                      className="fill-foreground text-3xl font-bold"
                    >
                      {totalOccurrences}
                    </tspan>
                    <tspan
                      x={viewBox.cx}
                      y={(viewBox.cy || 0) + 24}
                      className="fill-muted-foreground"
                    >
                      Occurrences
                    </tspan>
                  </text>
                );
              }
              return null;
            }}
          />
        </Pie>
      </PieChart>
    </ChartContainer>
  );
};

// Define chart configuration (for pie chart)
const chartConfig = {
  visitors: {
    label: "Occurrences",
  },
} satisfies ChartConfig;

// PieChartCard component (main component)
interface PieChartCardProps {
  data: FeederMessage[];
}

const PieChartCard = ({ data }: PieChartCardProps) => {
  // Memoized processing of data for the pie chart and finding the oldest timestamp
  const { processedData, oldestTimestamp } = useMemo(() => {
    const counts: { [key: string]: number } = {};
    let oldestTime: Date | null = null;

    data.forEach((message) => {
      // Get the prediction value and map it to the corresponding attack type
      const prediction = message.prediction;
      const attackType = invertedClassMap[prediction]?.name || "Unknown";

      // Increment the count for this attack type
      counts[attackType] = (counts[attackType] || 0) + 1;

      // Parse the timestamp and track the oldest one
      const timestamp = new Date(message.metadata.Timestamp);
      if (!oldestTime || timestamp < oldestTime) {
        oldestTime = timestamp;
      }
    });

    // Convert counts object into the format needed for the PieChart
    const processedData = Object.keys(counts).map((key) => ({
      name: key,
      value: counts[key],
      fill:
        invertedClassMap[classMap[key as keyof typeof classMap]?.value]
          ?.color || "gray", // Use corresponding color from classMap
    }));

    return {
      processedData,
      oldestTimestamp: oldestTime
        ? (oldestTime as Date).toLocaleString()
        : "N/A", // Format the oldest timestamp
    };
  }, [data]);

  return (
    <Card>
      <CardHeader>
        <CardTitle>Quick Summary</CardTitle>
        <CardDescription>
          <div>
            <p>Anomalies detected since network monitor started</p>
            <label className="font-bold italic">
              First packet received: {oldestTimestamp}
            </label>
          </div>
        </CardDescription>
      </CardHeader>
      <CardContent>
        {/* Render PieChartComponent with processed data */}
        <PieChartComponent data={processedData} />
      </CardContent>
    </Card>
  );
};

export default PieChartCard;
