import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  ResponsiveContainer,
} from "recharts";
import {
  Card,
  CardHeader,
  CardTitle,
  CardContent,
  CardDescription,
} from "@/components/ui/card";

// Sample function to generate a color for each new dataset
const generateColor = (index: number) => {
  const colors = [
    "rgba(255, 99, 132, 0.5)", // red
    "rgba(54, 162, 235, 0.5)", // blue
    "rgba(75, 192, 192, 0.5)", // green
    "rgba(255, 206, 86, 0.5)", // yellow
    "rgba(153, 102, 255, 0.5)", // purple
  ];
  return colors[index % colors.length];
};

// The PcapAreaChart component that will plot the data
const PcapAreaChart = ({ datasets }: { datasets: any[][] }) => {
  return (
    <ResponsiveContainer width="100%" height={400}>
      <AreaChart>
        <XAxis dataKey="time" />
        <YAxis />
        <Tooltip />
        <CartesianGrid stroke="#f5f5f5" />
        {/* Render each dataset as a separate Area */}
        {datasets.map((data, index) => (
          <Area
            key={index}
            type="monotone"
            dataKey="value"
            data={data}
            stroke={generateColor(index)}
            fill={generateColor(index)}
            isAnimationActive={false}
          />
        ))}
      </AreaChart>
    </ResponsiveContainer>
  );
};

export const PcapAreaChartCard = ({
  initialData,
}: {
  initialData: any[][];
}) => {
  return (
    <Card>
      <CardHeader>
        <CardTitle>PCAP Area Chart</CardTitle>
        <CardDescription>
          Visual representation of the incoming data.
        </CardDescription>
      </CardHeader>
      <CardContent>
        {/* Render the PcapAreaChart and pass datasets */}
        <PcapAreaChart datasets={initialData} />
      </CardContent>
    </Card>
  );
};

export default PcapAreaChartCard;
