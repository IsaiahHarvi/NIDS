import { createLazyFileRoute } from "@tanstack/react-router";
import { useStore } from "@/stores/bear-store";
import { Button } from "@/components/ui/button";
export const Route = createLazyFileRoute("/")({
  component: Index,
});

function Index() {
  const { count, inc } = useStore();
  return (
    <div className="p-2">
      <h3>Welcome Home!</h3>
      <div>
        <span>{count}</span>
        <Button onClick={inc}>one up</Button>
      </div>
    </div>
  );
}
