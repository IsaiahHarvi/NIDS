import { createFileRoute } from "@tanstack/react-router";

export const Route = createFileRoute("/help/")({
  component: () => (
    <div>
      Hello /help/!
      <button>click here</button>
    </div>
  ),
});
