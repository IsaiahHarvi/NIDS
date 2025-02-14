import { useState } from "react";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { ScrollArea } from "@/components/ui/scroll-area";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";

interface MetadataDialogProps {
  metadata: Record<string, string> | null | undefined;
}

export default function PcapMetaDataModal({ metadata }: MetadataDialogProps) {
  const [isOpen, setIsOpen] = useState(false);

  if (!metadata || Object.keys(metadata).length === 0) {
    return (
      <Button variant="outline" disabled>
        No Metadata Available
      </Button>
    );
  }

  return (
    <Dialog open={isOpen} onOpenChange={setIsOpen}>
      <DialogTrigger asChild>
        <Button variant="outline">View Metadata</Button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-[625px]">
        <DialogHeader>
          <DialogTitle>Metadata Information</DialogTitle>
          <DialogDescription>
            Detailed metadata for the selected item.
          </DialogDescription>
        </DialogHeader>
        <ScrollArea className="h-[400px] w-full rounded-md border p-4">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead className="w-[200px]">Property</TableHead>
                <TableHead>Value</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {Object.entries(metadata).map(([key, value]) => (
                <TableRow key={key}>
                  <TableCell className="font-medium">{key}</TableCell>
                  <TableCell>{value}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </ScrollArea>
      </DialogContent>
    </Dialog>
  );
}
