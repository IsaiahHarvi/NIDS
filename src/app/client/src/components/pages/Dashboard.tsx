import { useEffect, useState } from "react";
import { Card, CardHeader, CardTitle, CardDescription } from "../ui/card";
import PieChartCard from "../PieChart";
import { useServicesStore } from "@/stores/services-store";
import NetworkTableCard from "../NetworkTableCard";
import { Button } from "../ui/button";
import { startFeeders } from "@/middleware/api/functions/startFeeders";
import { stopFeeders } from "@/middleware/api/functions/stopFeeders";
import { useToast } from "@/hooks/use-toast";
import NetworkTrafficLineChart from "../NetworkTrafficLineChartCard";
import { Switch } from "../ui/switch";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "../ui/tabs";
import { getOfflineFeederReports } from "@/middleware/api/functions/getOfflineFeederReports";
import { getOfflineFeederReportById } from "@/middleware/api/functions/getOfflineFeederReportById";
import { sendReports } from "@/middleware/api/functions/sendReports";
import { useControlsStore } from "@/stores/controls-store";
import { FeederMessage } from "../../../../types/client-types";

const Dashboard = () => {
  const { toast } = useToast();
  const {
    offlineFeeders,
    feeders,
    setFeeders,
    setOfflineFeeders,
    setNeuralNetworks,
  } = useServicesStore();
  const {
    isOfflineFeeder,
    isFeedersStarted,
    isFeedersPaused,
    setIsOfflineFeeder,
    setIsFeedersStarted,
    setIsFeedersPaused,
  } = useControlsStore();

  const feederMode = isOfflineFeeder ? "offline_feeder" : "feeder";
  const [tabValue, setTabValue] = useState("current");
  const [tabData, setTabData] = useState<FeederMessage[]>([]);
  const [reportTabs, setReportTabs] = useState<
    { id: string; timestamp: string }[]
  >([]);

  useEffect(() => {
    const fetchReports = async () => {
      try {
        if (isOfflineFeeder) {
          const reports = await getOfflineFeederReports();
          setReportTabs(reports);
        } else {
          setReportTabs([]);
        }
      } catch (error) {
        console.error("Error fetching reports:", error);
      }
    };
    fetchReports();
  }, [isOfflineFeeder]);

  useEffect(() => {
    const fetchTabData = async () => {
      if (tabValue === "current") {
        setTabData(isOfflineFeeder ? Object.values(offlineFeeders) : feeders);
      } else if (isOfflineFeeder) {
        const report = await getOfflineFeederReportById(tabValue);
        if (report) {
          const messages = Object.values(report).filter(
            //eslint-disable-next-line
            (item: any): item is FeederMessage =>
              typeof item === "object" && "id_" in item
          );
          // @ts-expect-error: Type assertion for filtering FeederMessage objects
          setTabData(messages);
        } else {
          setTabData([]);
        }
      }
    };
    fetchTabData();
  }, [tabValue, offlineFeeders, feeders, isOfflineFeeder]);

  return (
    <div className="p-4">
      <Tabs defaultValue="current" value={tabValue} onValueChange={setTabValue}>
        <TabsList className="flex flex-wrap gap-2">
          <TabsTrigger value="current">Current</TabsTrigger>
          {isOfflineFeeder &&
            reportTabs.map((report) => (
              <TabsTrigger key={report.id} value={report.id}>
                {new Date(report.timestamp).toLocaleString()}
              </TabsTrigger>
            ))}
        </TabsList>

        <TabsContent value={tabValue}>
          <Card>
            <CardHeader>
              <CardTitle>Dashboard</CardTitle>
              <CardDescription>
                <div className="pt-3 flex flex-row justify-between items-center">
                  <span>Overview of your network and collected data</span>
                  <div className="flex gap-5">
                    <div className="flex items-center gap-2">
                      <span>{isOfflineFeeder ? "Test Feeder" : "Feeder"}</span>
                      <Switch
                        checked={isOfflineFeeder}
                        onCheckedChange={() =>
                          setIsOfflineFeeder(!isOfflineFeeder)
                        }
                        disabled={tabValue !== "current"}
                      />
                    </div>
                    <Button
                      size="sm"
                      onClick={() => {
                        if (!isFeedersStarted) {
                          startFeeders(feederMode);
                          setIsFeedersStarted(true);
                          setIsFeedersPaused(false);
                          toast({
                            title: "Feeders Started",
                            description: `Started ${feederMode} successfully`,
                            duration: 2000,
                          });
                        } else {
                          stopFeeders();
                          setIsFeedersPaused(true);
                          setIsFeedersStarted(false);
                          toast({
                            title: "Feeders Paused",
                            description:
                              "Feeders have been paused successfully",
                            duration: 2000,
                          });
                        }
                      }}
                      disabled={tabValue !== "current"}
                    >
                      {isFeedersStarted ? "Pause Feeders" : "Start Feeders"}
                    </Button>

                    <Button
                      size="sm"
                      disabled={
                        tabValue !== "current" ||
                        !isFeedersPaused ||
                        (offlineFeeders.length === 0 && feeders.length === 0)
                      }
                      onClick={() => {
                        sendReports(
                          feederMode,
                          feederMode === "offline_feeder"
                            ? offlineFeeders
                            : feeders
                        );
                        setFeeders([]);
                        setOfflineFeeders([]);
                        setNeuralNetworks([]);
                        setIsFeedersStarted(false);
                        setIsFeedersPaused(false);
                        toast({
                          title: "Feeders Reset",
                          description: "Feeders have been reset successfully",
                          duration: 2000,
                        });
                      }}
                    >
                      Complete Scan
                    </Button>
                  </div>
                </div>
              </CardDescription>
            </CardHeader>
          </Card>

          <div className="flex flex-row">
            <div className="pt-4 flex flex-row gap-4 w-1/5">
              <PieChartCard data={tabData} />
            </div>
            <div className="pt-4 pl-4 w-4/5">
              <NetworkTrafficLineChart data={tabData}></NetworkTrafficLineChart>
            </div>
          </div>
          <div className="pt-4">
            <NetworkTableCard data={tabData}></NetworkTableCard>
          </div>
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default Dashboard;
