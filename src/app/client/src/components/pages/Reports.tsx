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
import { Switch } from "@/components/ui/switch";
import { ChevronUp, ChevronDown } from "lucide-react";
import { format } from "date-fns";
import { getFeederReports } from "@/middleware/api/functions/getFeederReports";
import { getOfflineFeederReports } from "@/middleware/api/functions/getOfflineFeederReports";
import { getFeederReportById } from "@/middleware/api/functions/getFeederReportsById";
import { getOfflineFeederReportById } from "@/middleware/api/functions/getOfflineFeederReportById";
import jsPDF from "jspdf";
import autoTable from "jspdf-autotable";

type Report = { id: string; timestamp: string };
type ReportEntry = {
  id_?: string;
  prediction?: number;
  metadata?: {
    flow_start?: string;
  };
};

type SortDirection = "asc" | "desc";

// const classMap = {
//   benign: { value: 0, color: "green" },
//   malicious: { value: 1, color: "red" },
// };

export default function ReportsPage() {
  const [dateRange] = useState<{ from: Date; to: Date } | null>(null);
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

  const generatePDF = (report: Record<string, unknown>) => {
    const doc = new jsPDF();

    const currentDate = new Date().toLocaleString();
    const reportDate = new Date(report.timestamp as string).toLocaleString();
    doc.setFontSize(18);
    doc.text("Network Intrusion Detection Report", 14, 20);

    doc.setFontSize(12);
    doc.text(`Report Timestamp: ${reportDate}`, 14, 30);
    doc.text(`Generated on: ${currentDate}`, 14, 37);

    const entries: ReportEntry[] = Object.values(report).filter(
      (r): r is ReportEntry => typeof r === "object"
    );
    const totalEntries = entries.length;
    const maliciousCount = entries.filter((r) => r?.prediction === 1).length;
    const benignCount = totalEntries - maliciousCount;

    doc.setFontSize(16);
    doc.text("Summary", 14, 50);
    doc.setFontSize(12);
    doc.text(`Total Entries: ${totalEntries}`, 14, 60);
    doc.text(`Malicious: ${maliciousCount}`, 14, 67);
    doc.text(`Benign: ${benignCount}`, 14, 74);

    const tableData = entries.map((r, index) => [
      r.id_ || `Entry ${index + 1}`,
      r.metadata?.flow_start || "N/A",
      r.prediction === 1 ? "Malicious" : "Benign",
    ]);

    autoTable(doc, {
      startY: 80,
      head: [["ID", "Timestamp", "Status"]],
      body: tableData,
      theme: "striped",
      headStyles: {
        fillColor: [230, 126, 34],
        textColor: 255,
      },
    });

    doc.save(`network_intrusion_report_${report.id || "unknown"}.pdf`);
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
