"use client";

import { useMemo, useState } from "react";
import {
  Line,
  LineChart,
  Tooltip,
  XAxis,
  YAxis,
  ResponsiveContainer,
} from "recharts";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { ChevronDown, X } from "lucide-react";
import {
  DropdownMenu,
  DropdownMenuCheckboxItem,
  DropdownMenuContent,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";

import type { FeederMessage } from "../../../types/client-types";

const CustomTooltip = ({ active, payload, label }: any) => {
  if (active && payload && payload.length) {
    const data = payload[0].payload;
    return (
      <div className="p-3 bg-background border rounded-lg shadow-lg">
        <h4 className="font-semibold text-sm mb-1">{label}</h4>
        <p className="text-sm text-muted-foreground">
          Selected Metric Value:{" "}
          <span className="font-medium text-foreground">{data.value}</span>
        </p>
        <p className="text-sm text-muted-foreground">
          Source IP:{" "}
          <span className="font-medium text-foreground">{data.sourceIp}</span>
        </p>
      </div>
    );
  }
  return null;
};

const availableMetrics = [
  { label: "Total Forward Packets", key: "Total_Fwd_Packets" },
  { label: "Total Backward Packets", key: "Total_Backward_Packets" },
  { label: "Total Length of Fwd Packets", key: "Total_Length_of_Fwd_Packets" },
  { label: "Total Length of Bwd Packets", key: "Total_Length_of_Bwd_Packets" },
  { label: "Flow Bytes/s", key: "Flow_Bytes_s" },
  { label: "Flow Packets/s", key: "Flow_Packets_s" },
  { label: "Fwd IAT Mean", key: "Fwd_IAT_Mean" },
  { label: "Bwd IAT Mean", key: "Bwd_IAT_Mean" },
  { label: "Packet Length Mean", key: "Packet_Length_Mean" },
];

export default function NetworkTrafficLineChart({
  data,
}: {
  data: FeederMessage[] | null | undefined;
}) {
  const [selectedMetric, setSelectedMetric] = useState<string>(
    availableMetrics[0].key
  );
  const [selectedPoint, setSelectedPoint] = useState<any | null>(null);

  const chartData = useMemo(() => {
    if (!data || data.length === 0) {
      return [];
    }
    return data.map((message, index) => ({
      name: `Packet ${index + 1}`,
      value: parseFloat(message?.metadata?.[selectedMetric]) || 0,
      sourceIp: message?.metadata?.Source_IP || "Unknown",
    }));
  }, [data, selectedMetric]);

  const handleDotClick = (data: any) => {
    setSelectedPoint(data);
  };

  return (
    <Card className="w-full">
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle className="text-xl font-semibold">Network Traffic</CardTitle>
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button variant="outline" className="w-[240px] justify-between">
              {availableMetrics.find((m) => m.key === selectedMetric)?.label}
              <ChevronDown className="ml-2 h-4 w-4 opacity-50" />
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent className="w-[240px]">
            <DropdownMenuLabel>Select Metric</DropdownMenuLabel>
            <DropdownMenuSeparator />
            {availableMetrics.map((metric) => (
              <DropdownMenuCheckboxItem
                key={metric.key}
                checked={selectedMetric === metric.key}
                onCheckedChange={() => setSelectedMetric(metric.key)}
              >
                {metric.label}
              </DropdownMenuCheckboxItem>
            ))}
          </DropdownMenuContent>
        </DropdownMenu>
      </CardHeader>
      <CardContent className="pt-6">
        <div className="flex flex-col lg:flex-row gap-6">
          <div className="w-full lg:w-2/3 h-[400px]">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={chartData}>
                <XAxis
                  dataKey="name"
                  stroke="hsl(var(--muted-foreground))"
                  fontSize={12}
                  tickLine={false}
                  axisLine={false}
                />
                <YAxis
                  stroke="hsl(var(--muted-foreground))"
                  fontSize={12}
                  tickLine={false}
                  axisLine={false}
                  tickFormatter={(value) => `${value}`}
                />
                <Line
                  type="monotone"
                  dataKey="value"
                  stroke="hsl(var(--primary))"
                  strokeWidth={2}
                  dot={{
                    r: 4,
                    fill: "hsl(var(--primary))",
                    stroke: "hsl(var(--primary))",
                  }}
                  activeDot={{
                    r: 6,
                    onClick: (e: any, payload: any) => {
                      handleDotClick(payload.payload);
                    },
                  }}
                  isAnimationActive={false}
                />
                <Tooltip content={<CustomTooltip />} />
              </LineChart>
            </ResponsiveContainer>
          </div>

          <Card className="w-full lg:w-1/3">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">
                Selected Point Details
              </CardTitle>
              {selectedPoint && (
                <Button
                  variant="ghost"
                  size="icon"
                  onClick={() => setSelectedPoint(null)}
                  aria-label="Close details"
                >
                  <X className="h-4 w-4" />
                </Button>
              )}
            </CardHeader>
            <CardContent>
              {selectedPoint ? (
                <div className="space-y-2">
                  <p className="text-sm font-medium">
                    Packet: {selectedPoint.name}
                  </p>
                  <p className="text-sm text-muted-foreground">
                    Source IP:{" "}
                    <span className="font-medium text-foreground">
                      {selectedPoint.sourceIp}
                    </span>
                  </p>
                  <p className="text-sm text-muted-foreground">
                    Selected Metric Value:{" "}
                    <span className="font-medium text-foreground">
                      {selectedPoint.value}
                    </span>
                  </p>
                </div>
              ) : (
                <p className="text-sm text-muted-foreground">
                  Click on a data point in the chart to view details.
                </p>
              )}
            </CardContent>
          </Card>
        </div>
      </CardContent>
    </Card>
  );
}
