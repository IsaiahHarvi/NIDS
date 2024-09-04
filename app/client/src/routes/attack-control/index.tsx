import { createFileRoute } from "@tanstack/react-router";
import AttackControl from "../../components/pages/AttackControl";

export const Route = createFileRoute("/attack-control/")({
  component: () => (
    <div>
      <AttackControl />
    </div>
  ),
});
