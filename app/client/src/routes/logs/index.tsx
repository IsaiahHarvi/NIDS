import { createFileRoute } from "@tanstack/react-router";
import { Button } from "@/components/ui/button";

export const Route = createFileRoute("/logs/")({
  component: () => (
    <div className="p-8 max-w-3xl mx-auto font-sans">
      <Button>Clikc here</Button>
    </div>
  ),
});
