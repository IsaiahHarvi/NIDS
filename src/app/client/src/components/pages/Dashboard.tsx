import { Card, CardHeader, CardTitle, CardDescription } from "../ui/card";
// import PieChartComponent from "../PieChart";
import PieChartCard from "../PieChart";
// import PcapAreaChart from "../PcapAreaChart";
// import { ServicesState } from "@/stores/services-store";
import { useServicesStore } from "@/stores/services-store";
import { getFeeders } from "@/middleware/api/functions/getFeeders";
import { getOfflineFeeders } from "@/middleware/api/functions/getOfflineFeeders";
import { getNeuralNetworks } from "@/middleware/api/functions/getNeuralNetworks";
import { useEffect } from "react";
import NetworkFlowCard from "../NetworkFlowCard";
import NetworkTableCard from "../NetworkTableCard";
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
  const {
    feeders,
    setFeeders,
    offlineFeeders,
    setOfflineFeeders,
    neuralNetworks,
    setNeuralNetworks,
  } = useServicesStore();

  useEffect(() => {
    const fetchData = async () => {
      try {
        const fetchedFeeders = await getFeeders();
        setFeeders(fetchedFeeders);
        const fetchedOfflineFeeders = await getOfflineFeeders();
        setOfflineFeeders(fetchedOfflineFeeders);
        const fetchedNeuralNetworks = await getNeuralNetworks();
        setNeuralNetworks(fetchedNeuralNetworks);
      } catch (error) {
        console.error("Error fetching data: ", error);
      }
    };
    fetchData();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // console.log(feeders, offlineFeeders, neuralNetworks);
  console.log("feeders", feeders);
  console.log("offlineFeeders", offlineFeeders);
  console.log("neuralNetworks", neuralNetworks);

  const sampleData = [
    {
      id_: "1",
      input: [192, 168, 1, 1],
      prediction: 0,
      host: "192.168.1.100", // Host IP
      target: "10.0.0.1", // Target IP
      port: 80,
    },
    {
      id_: "2",
      input: [192, 168, 1, 2],
      prediction: 0,
      host: "192.168.1.100", // Same host as above
      target: "10.0.0.2", // Different Target IP
      port: 443,
    },
    {
      id_: "3",
      input: [192, 168, 1, 3],
      prediction: 0,
      host: "192.168.1.101", // Different host IP
      target: "10.0.0.3", // Different Target IP
      port: 8080,
    },
  ];

  return (
    <div className="p-4">
      <Card>
        <CardHeader>
          <CardTitle>Dashboard</CardTitle>
          <CardDescription>
            Overview of your network and collected data
          </CardDescription>
        </CardHeader>
        {/* <CardContent></CardContent> */}
      </Card>
      <div className="flex flex-row">
        <div className="pt-4 flex flex-row gap-4 w-1/5">
          <PieChartCard data={defaultChartData} />
        </div>
        <div className="pt-4 pl-4 w-4/5">
          <NetworkFlowCard data={sampleData} />
          <NetworkTableCard data={offlineFeeders}></NetworkTableCard>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
