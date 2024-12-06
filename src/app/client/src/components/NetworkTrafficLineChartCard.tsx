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

interface TooltipPayload {
  payload: {
    name: string;
    value: number;
    src_ip: string;
    dst_ip: string;
    src_port: number;
    dst_port: number;
  };
}

interface CustomTooltipProps {
  active?: boolean;
  payload?: TooltipPayload[] | null;
  label?: string;
}

const CustomTooltip = ({ active, payload, label }: CustomTooltipProps) => {
  if (active && payload && payload.length) {
    const data = payload[0].payload;
    return (
      <div className="p-3 bg-background border rounded-lg shadow-lg">
        <h4 className="font-semibold text-sm mb-1">{label}</h4>
        <p className="text-sm text-muted-foreground">
          Metric Value:{" "}
          <span className="font-medium text-foreground">{data.value}</span>
        </p>
        <p className="text-sm text-muted-foreground">
          Source IP:{" "}
          <span className="font-medium text-foreground">{data.src_ip}</span>
        </p>
        <p className="text-sm text-muted-foreground">
          Destination IP:{" "}
          <span className="font-medium text-foreground">{data.dst_ip}</span>
        </p>
        <p className="text-sm text-muted-foreground">
          Source Port:{" "}
          <span className="font-medium text-foreground">{data.src_port}</span>
        </p>
        <p className="text-sm text-muted-foreground">
          Destination Port:{" "}
          <span className="font-medium text-foreground">{data.dst_port}</span>
        </p>
      </div>
    );
  }
  return null;
};

const availableMetrics = [
  { label: "Bidirectional Packets", key: "bidirectional_packets" },
  { label: "Bidirectional Bytes", key: "bidirectional_bytes" },
  { label: "Bidirectional Duration (ms)", key: "bidirectional_duration_ms" },
  { label: "Source to Destination Packets", key: "src2dst_packets" },
  { label: "Destination to Source Packets", key: "dst2src_packets" },
];

interface ChartData {
  name: string;
  value: number;
  src_ip: string;
  dst_ip: string;
  src_port: number;
  dst_port: number;
}

export default function NetworkTrafficLineChart({
  data,
}: {
  data: FeederMessage[] | null | undefined;
}) {
  const [selectedMetric, setSelectedMetric] = useState<string>(
    availableMetrics[0].key
  );
  const [selectedPoint, setSelectedPoint] = useState<ChartData | null>(null);

  const chartData: ChartData[] = useMemo(() => {
    if (!data || data.length === 0) {
      return [];
    }
    return data.map((message, index) => ({
      name: `Packet ${index + 1}`,
      value: parseFloat(message?.metadata?.[selectedMetric]) || 0,
      src_ip: message?.metadata?.src_ip || "Unknown",
      dst_ip: message?.metadata?.dst_ip || "Unknown",
      src_port: parseInt(message?.metadata?.src_port) || 0,
      dst_port: parseInt(message?.metadata?.dst_port) || 0,
    }));
  }, [data, selectedMetric]);

  const handleDotClick = (data: ChartData) => {
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
                    onClick: (
                      e: React.MouseEvent<SVGCircleElement, MouseEvent> & {
                        payload: ChartData;
                      }
                    ) => {
                      if (e && e.payload) {
                        handleDotClick(e.payload as ChartData);
                      }
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
                      {selectedPoint.src_ip}
                    </span>
                  </p>
                  <p className="text-sm text-muted-foreground">
                    Destination IP:{" "}
                    <span className="font-medium text-foreground">
                      {selectedPoint.dst_ip}
                    </span>
                  </p>
                  <p className="text-sm text-muted-foreground">
                    Source Port:{" "}
                    <span className="font-medium text-foreground">
                      {selectedPoint.src_port}
                    </span>
                  </p>
                  <p className="text-sm text-muted-foreground">
                    Destination Port:{" "}
                    <span className="font-medium text-foreground">
                      {selectedPoint.dst_port}
                    </span>
                  </p>
                  <p className="text-sm text-muted-foreground">
                    Metric Value:{" "}
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
