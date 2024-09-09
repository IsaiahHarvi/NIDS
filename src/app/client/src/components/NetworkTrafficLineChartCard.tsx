"use client";

import { useMemo, useState } from "react";
import { Line, LineChart, Tooltip, XAxis, YAxis } from "recharts";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { X } from "lucide-react";

import type { FeederMessage } from "../../../types/client-types";

const CustomTooltip = ({ active, payload, label }: any) => {
  if (active && payload && payload.length) {
    const data = payload[0].payload;
    return (
      <div className="p-2 bg-background border rounded shadow-sm">
        <h4 className="font-semibold">{label}</h4>
        <p>Total Forward Packets: {data.totalFwdPackets}</p>
        <p>Source IP: {data.sourceIp}</p>
      </div>
    );
  }
  return null;
};

export function NetworkTrafficLineChart({ data }: { data: FeederMessage[] }) {
  const [selectedPoint, setSelectedPoint] = useState<any | null>(null);

  const chartData = useMemo(() => {
    return data.map((message, index) => ({
      name: `Packet ${index + 1}`,
      totalFwdPackets: parseInt(message.metadata.Total_Fwd_Packets, 10) || 0,
      sourceIp: message.metadata.Source_IP,
    }));
  }, [data]);

  const handleDotClick = (data: any) => {
    setSelectedPoint(data);
  };

  return (
    <div className="flex space-x-4">
      <Card className="flex-grow">
        <CardHeader>
          <CardTitle>Network Traffic (Total Forward Packets)</CardTitle>
        </CardHeader>
        <CardContent className="flex gap-4">
          <div className="w-full h-[400px]">
            {" "}
            {/* Adjusted height and full width */}
            <LineChart
              width={800} // Set desired width explicitly to avoid warning
              height={400} // Adjust height accordingly
              data={chartData}
            >
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
                dataKey="totalFwdPackets"
                stroke="hsl(var(--primary))"
                strokeWidth={2}
                activeDot={{
                  onClick: (e: any, payload: any) => {
                    handleDotClick(payload.payload);
                  },
                }}
                isAnimationActive={false}
              />
              <Tooltip content={<CustomTooltip />} />
            </LineChart>
          </div>

          <Card className="w-1/3">
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
            {selectedPoint && (
              <CardContent>
                <div className="space-y-2">
                  <p className="text-sm font-medium">
                    Packet: {selectedPoint.name}
                  </p>
                  <p className="text-sm">Source IP: {selectedPoint.sourceIp}</p>
                  <p className="text-sm">
                    Total Forward Packets: {selectedPoint.totalFwdPackets}
                  </p>
                </div>
              </CardContent>
            )}
          </Card>
        </CardContent>
      </Card>
    </div>
  );
}

export default NetworkTrafficLineChart;
