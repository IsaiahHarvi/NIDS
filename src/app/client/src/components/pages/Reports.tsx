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
import jsPDF from "jspdf";
import autoTable from "jspdf-autotable";

type Report = { id: string; timestamp: string };

type SortDirection = "asc" | "desc";

const classMap = {
  BENIGN: { value: 0, color: "green" },
  PortScan: { value: 9, color: "yellow" },
  "FTP-Patator": { value: 7, color: "yellow" },
  "SSH-Patator": { value: 10, color: "yellow" },
  "DoS slowloris": { value: 4, color: "orange" },
  "DoS Slowhttptest": { value: 5, color: "orange" },
  "DoS GoldenEye": { value: 3, color: "orange" },
  "DoS Hulk": { value: 4, color: "orange" },
  Bot: { value: 1, color: "red" },
  Heartbleed: { value: 8, color: "red" },
  DDoS: { value: 2, color: "red" },
};

export default function ReportsPage() {
  const [dateRange, setDateRange] = useState<{ from: Date; to: Date } | null>(
    null
  );
  const [sortColumn, setSortColumn] = useState<string>("timestamp");
  const [sortDirection, setSortDirection] = useState<SortDirection>("desc");
  const [reports, setReports] = useState<Report[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [isOfflineFeeder, setIsOfflineFeeder] = useState<boolean>(true);

  const [attackSummary, setAttackSummary] = useState<{
    totalReports: number;
  }>({
    totalReports: 0,
  });

  useEffect(() => {
    async function fetchReports() {
      setLoading(true);
      try {
        let fetchedReports = [];
        if (isOfflineFeeder) {
          fetchedReports = await getOfflineFeederReports();
        } else {
          fetchedReports = await getFeederReports();
        }
        setReports(fetchedReports);

        setAttackSummary({
          totalReports: fetchedReports.length,
        });
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
    try {
      const report = isOfflineFeeder
        ? await getOfflineFeederReportById(id)
        : await getFeederReportById(id);

      if (report) {
        generatePDF(report);
      } else {
        console.error("Report not found");
      }
    } catch (error) {
      console.error("Error downloading report:", error);
    }
  };

  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const generatePDF = (report: any) => {
    const doc = new jsPDF();

    const currentDate = new Date().toLocaleString();
    const reportDate = new Date(report.timestamp).toLocaleString();
    doc.setFontSize(18);
    doc.text("Network Intrusion Detection Report", 14, 20);

    doc.setFontSize(12);
    doc.text(`Report Timestamp: ${reportDate}`, 14, 30);
    doc.text(`Generated on: ${currentDate}`, 14, 37);

    doc.setFontSize(16);
    doc.text("Malicious Attacks Summary", 14, 50);

    const maliciousReports = Object.values(report)
      .filter(
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        (r: any) =>
          r.prediction !== classMap.BENIGN.value && r.metadata !== undefined
      )
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      .map((r: any) => {
        const attackType =
          (Object.keys(classMap) as (keyof typeof classMap)[]).find(
            (key) => classMap[key].value === r.prediction
          ) || "Unknown";

        return {
          attackType,
          sourceIP: r.metadata.Source_IP || "N/A",
          destinationIP: r.metadata.Destination_IP || "N/A",
        };
      });

    if (maliciousReports.length > 0) {
      const maliciousData = maliciousReports.map((r) => [
        r.attackType,
        r.sourceIP,
        r.destinationIP,
      ]);

      autoTable(doc, {
        startY: 55,
        head: [["Attack Type", "Source IP", "Destination IP"]],
        body: maliciousData,
        theme: "striped",
        headStyles: {
          fillColor: [230, 126, 34],
          textColor: 255,
        },
      });
    } else {
      doc.setFontSize(12);
      doc.text("No malicious attacks detected.", 14, 60);
    }

    const lastY = doc.lastAutoTable ? doc.lastAutoTable.finalY + 10 : 75;
    doc.setFontSize(16);
    doc.text("Report Metadata", 14, lastY);

    if (report.metadata) {
      const metadataEntries = [
        ["Source IP", report.metadata.Source_IP || "N/A"],
        ["Source Port", report.metadata.Source_Port || "N/A"],
        ["Destination IP", report.metadata.Destination_IP || "N/A"],
        ["Destination Port", report.metadata.Destination_Port || "N/A"],
        ["Protocol", report.metadata.Protocol || "N/A"],
        ["Flow Duration", `${report.metadata.Flow_Duration || 0} ms`],
      ];

      autoTable(doc, {
        startY: lastY + 5,
        head: [["Field", "Value"]],
        body: metadataEntries,
        theme: "striped",
        headStyles: {
          fillColor: [41, 128, 185],
          textColor: 255,
        },
      });
    } else {
      doc.setFontSize(12);
      doc.text("No metadata available.", 14, lastY + 5);
    }

    doc.save(`network_intrusion_report_${report.id_ || "unknown"}.pdf`);
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
            <>
              <div className="mb-4">
                <p>
                  <strong>Attack Summary:</strong>
                </p>
                <p>Total Reports: {attackSummary.totalReports}</p>
              </div>
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
            </>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
