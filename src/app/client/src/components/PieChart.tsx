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

// Define the type for the pie chart prop
interface PieChartComponentProps {
  data: string[];
}

// PieChartComponent implementation (subcomponent)
const PieChartComponent = ({ data }: PieChartComponentProps) => {
  // Process the array of strings and count the occurrences
  const processedData = useMemo(() => {
    const counts: { [key: string]: number } = {};

    data.forEach((item) => {
      counts[item] = (counts[item] || 0) + 1;
    });

    return Object.keys(counts).map((key) => ({
      name: key,
      value: counts[key],
      fill: `hsl(var(--chart-${Math.floor(Math.random() * 5) + 1}))`, // Example random color
    }));
  }, [data]);

  const totalOccurrences = useMemo(() => {
    return processedData.reduce((acc, curr) => acc + curr.value, 0);
  }, [processedData]);

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
          data={processedData}
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
  data: string[];
}

const PieChartCard = ({ data }: PieChartCardProps) => {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Quick Summary</CardTitle>
        <CardDescription>
          <div>
            <p>Anomalies detected since network monitor started</p>
            <label className="font-bold italic">
              First packet received: 12:45
            </label>
          </div>
        </CardDescription>
      </CardHeader>
      <CardContent>
        {/* Render PieChartComponent with passed data */}
        <PieChartComponent data={data} />
      </CardContent>
    </Card>
  );
};

export default PieChartCard;
