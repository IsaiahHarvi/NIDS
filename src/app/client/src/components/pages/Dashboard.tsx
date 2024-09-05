import {
  Card,
  CardHeader,
  CardTitle,
  CardContent,
  CardDescription,
} from "../ui/card";
// import PieChartComponent from "../PieChart";
import PieChartCard from "../PieChart";

const defaultChartData = [
  "Bot",
  "Bot",
  "Bot",
  "Bot",
  "Bot",
  "Bot",
  "Bot",
  "Bot",
  "Bot",
  "DoS GoldenEye",
  "DoS GoldenEye",
  "DoS GoldenEye",
  "DoS GoldenEye",
  "DoS GoldenEye",
  "DoS GoldenEye",
  "DoS GoldenEye",
  "DoS Hulk",
  "DoS Hulk",
  "DoS Hulk",
  "DoS Hulk",
  "DoS Hulk",
  "DoS Hulk",
  "DoS Slowhttptest",
  "DoS Slowhttptest",
  "DoS Slowhttptest",
  "DoS Slowhttptest",
  "DoS Slowhttptest",
  "DoS slowloris",
  "DoS slowloris",
  "DoS slowloris",
  "DoS slowloris",
  "FTP-Patator",
  "FTP-Patator",
  "Heartbleed",
  "Heartbleed",
  "Heartbleed",
  "Heartbleed",
  "Heartbleed",
  "Heartbleed",
  "Heartbleed",
  "Heartbleed",
  "Infiltration",
  "Infiltration",
  "Infiltration",
  "Infiltration",
  "Infiltration",
  "Infiltration",
  "Infiltration",
  "Infiltration",
  "Infiltration",
  "Infiltration",
  "PortScan",
  "SSH-Patator",
  "SSH-Patator",
  "SSH-Patator",
];

const Dashboard = () => {
  return (
    // <div className="p-4 flex flex-col lg:flex-row gap-4">
    <div className="p-4 ">
      <Card>
        <CardHeader>
          <CardTitle>Dashboard</CardTitle>
          <CardDescription>
            Overview of your network and collected data
          </CardDescription>
        </CardHeader>
        <CardContent>
          {/* <p>Overview of collected data</p> */}
          {/* <PieChartComponent data={["A", "B", "C", "D", "E"]} /> */}
        </CardContent>
      </Card>
      <div className="pt-4 flex flex-row gap-4 w-1/5">
        <PieChartCard data={defaultChartData} />
      </div>
    </div>
  );
};

export default Dashboard;
