"use client";

import { useState, useEffect } from "react";
import {
  Card,
  CardHeader,
  CardTitle,
  CardDescription,
  CardContent,
} from "@/components/ui/card";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Button } from "@/components/ui/button";
import { Calendar } from "@/components/ui/calendar";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";
import { Switch } from "@/components/ui/switch";
import { CalendarIcon, ChevronUp, ChevronDown } from "lucide-react";
import { format } from "date-fns";
import { getFeederReports } from "@/middleware/api/functions/getFeederReports";
import { getOfflineFeederReports } from "@/middleware/api/functions/getOfflineFeederReports";
import { getFeederReportById } from "@/middleware/api/functions/getFeederReportsById";
import { getOfflineFeederReportById } from "@/middleware/api/functions/getOfflineFeederReportById";
type Report = { id: string; timestamp: string };

type SortDirection = "asc" | "desc";

export default function ReportsPage() {
  const [dateRange, setDateRange] = useState<{ from: Date; to: Date } | null>(
    null
  );
  const [sortColumn, setSortColumn] = useState<string>("timestamp");
  const [sortDirection, setSortDirection] = useState<SortDirection>("desc");
  const [reports, setReports] = useState<Report[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [isOfflineFeeder, setIsOfflineFeeder] = useState<boolean>(true); // Switch state

  // Fetch reports based on the switch state
  useEffect(() => {
    async function fetchReports() {
      setLoading(true);
      try {
        if (isOfflineFeeder) {
          const offlineReports = await getOfflineFeederReports();
          setReports(offlineReports);
        } else {
          const feederReports = await getFeederReports();
          setReports(feederReports);
        }
      } catch (error) {
        console.error("Error fetching reports:", error);
      } finally {
        setLoading(false);
      }
    }
    fetchReports();
  }, [isOfflineFeeder]);

  const handleSort = (column: string) => {
    if (column === sortColumn) {
      setSortDirection(sortDirection === "asc" ? "desc" : "asc");
    } else {
      setSortColumn(column);
      setSortDirection("asc");
    }
  };

  const handleDownload = async (id: string) => {
    console.log(id);
    try {
      const report = isOfflineFeeder
        ? await getOfflineFeederReportById(id)
        : await getFeederReportById(id);

      if (report) {
        console.log("Fetched Report:", report);
        // Add your logic to handle the downloaded report, e.g., save as PDF
      } else {
        console.error("Report not found");
      }
    } catch (error) {
      console.error("Error downloading report:", error);
    }
  };

  const sortedReports = [...reports].sort((a, b) => {
    if (sortColumn === "timestamp") {
      return sortDirection === "asc"
        ? new Date(a.timestamp).getTime() - new Date(b.timestamp).getTime()
        : new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime();
    }
    return 0;
  });

  const filteredReports = sortedReports.filter((report) => {
    const reportDate = new Date(report.timestamp);
    return (
      !dateRange || (reportDate >= dateRange.from && reportDate <= dateRange.to)
    );
  });

  return (
    <div className="p-4">
      <Card>
        <CardHeader>
          <CardTitle>Reports</CardTitle>
          <CardDescription>
            View and download automatically generated reports
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="flex justify-between items-center mb-4">
            <div className="flex items-center space-x-4">
              <Switch
                checked={isOfflineFeeder}
                onCheckedChange={() => setIsOfflineFeeder((prev) => !prev)}
              />
              <span>
                {isOfflineFeeder ? "Offline Feeder Reports" : "Feeder Reports"}
              </span>
            </div>
            <div className="flex space-x-4">
              <Popover>
                <PopoverTrigger asChild>
                  <Button
                    variant="outline"
                    className="w-[300px] justify-start text-left font-normal"
                  >
                    <CalendarIcon className="mr-2 h-4 w-4" />
                    {dateRange ? (
                      <>
                        {format(dateRange.from, "LLL dd, y")} -{" "}
                        {format(dateRange.to, "LLL dd, y")}
                      </>
                    ) : (
                      <span>Pick a date range</span>
                    )}
                  </Button>
                </PopoverTrigger>
                <PopoverContent className="w-auto p-0" align="start">
                  <Calendar
                    initialFocus
                    mode="range"
                    selected={dateRange || undefined}
                    onSelect={(range: { from?: Date; to?: Date } | undefined) =>
                      setDateRange(
                        range?.from && range?.to
                          ? { from: range.from, to: range.to }
                          : null
                      )
                    }
                    numberOfMonths={2}
                  />
                </PopoverContent>
              </Popover>
            </div>
          </div>
          {loading ? (
            <p>Loading...</p>
          ) : (
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead
                    className="cursor-pointer"
                    onClick={() => handleSort("timestamp")}
                  >
                    Date
                    {sortColumn === "timestamp" &&
                      (sortDirection === "asc" ? (
                        <ChevronUp className="inline ml-2" />
                      ) : (
                        <ChevronDown className="inline ml-2" />
                      ))}
                  </TableHead>
                  <TableHead>Action</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {filteredReports.map((report) => (
                  <TableRow key={report.id}>
                    <TableCell>
                      {format(new Date(report.timestamp), "PPpp")}
                    </TableCell>
                    <TableCell>
                      {/* {console.log(report.id)} */}
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => handleDownload(report.id)}
                      >
                        Download
                      </Button>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
