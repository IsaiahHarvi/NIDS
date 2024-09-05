import { Card, CardHeader, CardTitle, CardDescription } from "../ui/card";
// import PieChartComponent from "../PieChart";
import PieChartCard from "../PieChart";
import PcapAreaChart from "../PcapAreaChart";
// import { ServicesState } from "@/stores/services-store";
import { useServicesStore } from "@/stores/services-store";
import { getFeeders } from "@/middleware/api/functions/getFeeders";
import { getOfflineFeeders } from "@/middleware/api/functions/getOfflineFeeders";
import { getNeuralNetworks } from "@/middleware/api/functions/getNeuralNetworks";
import { useEffect } from "react";
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
  }, []);

  // console.log(feeders, offlineFeeders, neuralNetworks);
  console.log("feeders", feeders);
  console.log("offlineFeeders", offlineFeeders);
  console.log("neuralNetworks", neuralNetworks);

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
          <PcapAreaChart
            initialData={[
              [
                { time: 1, value: 100 },
                { time: 2, value: 200 },
                { time: 3, value: 150 },
              ],
              [
                { time: 1, value: 50 },
                { time: 2, value: 120 },
                { time: 3, value: 180 },
              ],
            ]}
          />
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
