import { Card, CardHeader, CardTitle, CardDescription } from "../ui/card";
import PieChartCard from "../PieChart";
import { useServicesStore } from "@/stores/services-store";
import NetworkTableCard from "../NetworkTableCard";
import { Button } from "../ui/button";
import { startFeeders } from "@/middleware/api/functions/startFeeders";
import { stopFeeders } from "@/middleware/api/functions/stopFeeders";
import { useToast } from "@/hooks/use-toast";
import NetworkTrafficLineChart from "../NetworkTrafficLineChartCard";
import { useState } from "react";
import { Switch } from "../ui/switch";

const Dashboard = () => {
  const { toast } = useToast();
  const { offlineFeeders } = useServicesStore();
  const [isOfflineFeeder, setIsOfflineFeeder] = useState(true);

  const feederMode = isOfflineFeeder ? "offline_feeder" : "feeder";
  return (
    <div className="p-4">
      <Card>
        <CardHeader>
          <CardTitle>Dashboard</CardTitle>
          <CardDescription>
            <div className="pt-3 flex flex-row justify-between items-center">
              <span>Overview of your network and collected data</span>
              <div className="flex gap-5">
                {/*Switch between feeder modes*/}
                <div className="flex items-center gap-2">
                  <span>{isOfflineFeeder ? "Test Feeder" : "Feeder"}</span>
                  <Switch
                    checked={isOfflineFeeder}
                    onCheckedChange={() => setIsOfflineFeeder((prev) => !prev)}
                  />
                </div>

                <Button
                  size={"sm"}
                  onClick={() => {
                    startFeeders(feederMode);
                    toast({
                      title: "Feeders Started",
                      description: `Started ${feederMode} successfully`,
                      duration: 2000,
                    });
                  }}
                >
                  Start Feeders
                </Button>

                <Button
                  size={"sm"}
                  onClick={() => {
                    stopFeeders();
                    toast({
                      title: "Feeders Stopped",
                      description: "Feeders have been stopped successfully",
                      duration: 2000,
                    });
                  }}
                >
                  Stop
                </Button>
              </div>
            </div>
          </CardDescription>
        </CardHeader>
      </Card>

      <div className="flex flex-row">
        <div className="pt-4 flex flex-row gap-4 w-1/5">
          <PieChartCard data={offlineFeeders} />
        </div>
        <div className="pt-4 pl-4 w-4/5">
          <NetworkTrafficLineChart
            data={offlineFeeders}
          ></NetworkTrafficLineChart>
        </div>
      </div>
      <div className="pt-4">
        <NetworkTableCard data={offlineFeeders}></NetworkTableCard>
      </div>
    </div>
  );
};

export default Dashboard;
