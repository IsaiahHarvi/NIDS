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
  PortScan: { value: 1, color: "yellow" },
  "FTP-Patator": { value: 2, color: "yellow" },
  "SSH-Patator": { value: 3, color: "yellow" },
  "DoS slowloris": { value: 4, color: "orange" },
  "DoS Slowhttptest": { value: 5, color: "orange" },
  "DoS GoldenEye": { value: 6, color: "orange" },
  "DoS Hulk": { value: 7, color: "orange" },
  Heartbleed: { value: 8, color: "red" },
  Bot: { value: 9, color: "red" },
  Infiltration: { value: 10, color: "red" },
  DDoS: { value: 11, color: "red" },
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
    if (!data || data.length === 0) return 0;
    return data.reduce((acc, curr) => acc + curr.value, 0);
  }, [data]);

  if (!data || data.length === 0) {
    return (
      <div className="text-center">
        <p>No data available to display the chart.</p>
      </div>
    );
  }

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

const chartConfig = {
  visitors: {
    label: "Occurrences",
  },
} satisfies ChartConfig;

interface PieChartCardProps {
  data: FeederMessage[] | null | undefined;
}

const PieChartCard = ({ data }: PieChartCardProps) => {
  const { processedData, oldestTimestamp } = useMemo(() => {
    const counts: { [key: string]: number } = {};
    let oldestTime: Date | null = null;

    if (!data || data.length === 0) {
      return {
        processedData: [],
        oldestTimestamp: "N/A",
      };
    }

    data.forEach((message) => {
      const prediction = message.prediction;
      const attackType = invertedClassMap[prediction]?.name || "Unknown";

      counts[attackType] = (counts[attackType] || 0) + 1;

      const timestamp = new Date(message?.metadata?.Timestamp);
      if (!oldestTime || timestamp < oldestTime) {
        oldestTime = timestamp;
      }
    });

    const processedData = Object.keys(counts).map((key) => ({
      name: key,
      value: counts[key],
      fill:
        invertedClassMap[classMap[key as keyof typeof classMap]?.value]
          ?.color || "gray",
    }));

    return {
      processedData,
      oldestTimestamp: oldestTime
        ? (oldestTime as Date).toLocaleString()
        : "N/A",
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
        <PieChartComponent data={processedData} />
      </CardContent>
    </Card>
  );
};

export default PieChartCard;
