"use client";

import { useState } from "react";
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
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Calendar } from "@/components/ui/calendar";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";
import { CalendarIcon, Download, ChevronUp, ChevronDown } from "lucide-react";
import { format } from "date-fns";

// Define the Severity type
type Severity = "Low" | "Medium" | "High";
type SeverityFilter = Severity | "All"; // Include "All" as a valid option

// Mock data for reports
const mockReports: { id: number; date: string; severity: Severity }[] = [
  { id: 1, date: "2024-03-01", severity: "High" },
  { id: 2, date: "2024-02-28", severity: "Low" },
  { id: 3, date: "2024-02-27", severity: "Medium" },
  { id: 4, date: "2024-02-26", severity: "High" },
  { id: 5, date: "2024-02-25", severity: "Low" },
  { id: 6, date: "2024-02-24", severity: "Medium" },
  { id: 7, date: "2024-02-23", severity: "High" },
  { id: 8, date: "2024-02-22", severity: "Low" },
  { id: 9, date: "2024-02-21", severity: "Medium" },
  { id: 10, date: "2024-02-20", severity: "High" },
  { id: 11, date: "2024-02-19", severity: "Low" },
  { id: 12, date: "2024-02-18", severity: "Medium" },
  { id: 13, date: "2024-02-17", severity: "High" },
  { id: 14, date: "2024-02-16", severity: "Low" },
  { id: 15, date: "2024-02-15", severity: "Medium" },
];

type SortDirection = "asc" | "desc";

export default function ReportsPage() {
  const [dateRange, setDateRange] = useState<{ from: Date; to: Date } | null>(
    null
  );
  const [selectedSeverity, setSelectedSeverity] =
    useState<SeverityFilter>("All");
  const [sortColumn, setSortColumn] = useState<string>("date");
  const [sortDirection, setSortDirection] = useState<SortDirection>("desc");

  const handleDownload = (reportId: number) => {
    console.log(`Downloading report ${reportId}`);
  };

  const handleSort = (column: string) => {
    if (column === sortColumn) {
      setSortDirection(sortDirection === "asc" ? "desc" : "asc");
    } else {
      setSortColumn(column);
      setSortDirection("asc");
    }
  };

  const severityOrder: Record<Severity, number> = {
    Low: 1,
    Medium: 2,
    High: 3,
  };

  const sortedReports = [...mockReports].sort((a, b) => {
    if (sortColumn === "date") {
      return sortDirection === "asc"
        ? a.date.localeCompare(b.date)
        : b.date.localeCompare(a.date);
    } else if (sortColumn === "severity") {
      return sortDirection === "asc"
        ? severityOrder[a.severity] - severityOrder[b.severity]
        : severityOrder[b.severity] - severityOrder[a.severity];
    }
    return 0;
  });

  const filteredReports = sortedReports.filter((report) => {
    const reportDate = new Date(report.date);
    return (
      (selectedSeverity === "All" || report.severity === selectedSeverity) &&
      (!dateRange ||
        (reportDate >= dateRange.from && reportDate <= dateRange.to))
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
              <Select
                onValueChange={(value) =>
                  setSelectedSeverity(value as SeverityFilter)
                }
              >
                <SelectTrigger className="w-[180px]">
                  <SelectValue placeholder="Select severity" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="All">All Severities</SelectItem>
                  <SelectItem value="Low">Low</SelectItem>
                  <SelectItem value="Medium">Medium</SelectItem>
                  <SelectItem value="High">High</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead
                  className="cursor-pointer"
                  onClick={() => handleSort("date")}
                >
                  Date
                  {sortColumn === "date" &&
                    (sortDirection === "asc" ? (
                      <ChevronUp className="inline ml-2" />
                    ) : (
                      <ChevronDown className="inline ml-2" />
                    ))}
                </TableHead>
                <TableHead
                  className="cursor-pointer"
                  onClick={() => handleSort("severity")}
                >
                  Severity
                  {sortColumn === "severity" &&
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
                  <TableCell>{report.date}</TableCell>
                  <TableCell>
                    <span
                      className={`px-2 py-1 rounded-full text-xs font-medium
                      ${
                        report.severity === "Low"
                          ? "bg-green-100 text-green-800"
                          : report.severity === "Medium"
                            ? "bg-yellow-100 text-yellow-800"
                            : "bg-red-100 text-red-800"
                      }`}
                    >
                      {report.severity}
                    </span>
                  </TableCell>
                  <TableCell>
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => handleDownload(report.id)}
                    >
                      <Download className="mr-2 h-4 w-4" />
                      Download PDF
                    </Button>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </div>
  );
}
