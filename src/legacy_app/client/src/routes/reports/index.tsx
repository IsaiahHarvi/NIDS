import { createFileRoute } from "@tanstack/react-router";
import Reports from "@/components/pages/Reports";

export const Route = createFileRoute("/reports/")({
  component: () => (
    <div>
      <Reports />
    </div>
  ),
});
