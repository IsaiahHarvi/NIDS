import { createLazyFileRoute } from "@tanstack/react-router";
// import { useStore } from "@/stores/bear-store";
// import { Button } from "@/components/ui/button";

import {
  Card,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import Balancer from "react-wrap-balancer";
import type { LucideIcon } from "lucide-react";
import { Sparkles, Crosshair, ScrollText, Gamepad2 } from "lucide-react";
import { Link } from "@tanstack/react-router";

export const Route = createLazyFileRoute("/")({
  component: Index,
});

// function Index() {
//   const { count, inc } = useStore();
//   return (
//     <div className="p-2">
//       <h3>Welcome Home!</h3>
//       <div>
//         <span>{count}</span>
//         <Button onClick={inc}>one up</Button>
//       </div>
//     </div>
//   );
// }

export function Index() {
  return (
    <div className="container relative  justify-center py-8">
      <div className="mx-auto flex max-w-[980px] flex-col items-center gap-2 py-0 ">
        <div className="text-center text-3xl font-bold leading-tight tracking-tighter md:text-5xl lg:leading-[1.1]">
          NIDS
        </div>
        <Balancer className="max-w-[750px] text-center text-lg font-light text-foreground">
          Network Intrustion Detection System
        </Balancer>
      </div>
      <div className="text-base sm:pl-2 md:pl-8 ">
        <p className="py-2 text-xl sm:text-2xl lg:text-4xl"></p>
      </div>
      <div className="grid grid-cols-2 lg:grid-cols-3 gap-4">
        <LinkCard
          icon={Gamepad2}
          title="Controls"
          description="NIDS Controls"
          link="/help"
        />
        <LinkCard
          icon={ScrollText}
          title="Log Page"
          description="View the data from various components"
          link="/logs"
        />
        <LinkCard
          icon={Crosshair}
          title="test"
          description="test page"
          link="/test"
        />
        <LinkCard
          icon={Sparkles}
          title="Status"
          description="View the status of NIDS"
          link="/status"
        />
      </div>
    </div>
  );
}
function LinkCard({
  title,
  description,
  link,
  icon: Icon,
}: {
  title: string;
  description: string;
  link: string;
  icon: LucideIcon;
}) {
  return (
    <Link to={link}>
      <Card>
        <CardHeader>
          <CardTitle>
            <div className="flex flex-row items-center ">
              <Icon className="h-6 w-14 text-inherit" />
              {title}
            </div>
          </CardTitle>
          <CardDescription>{description}</CardDescription>
        </CardHeader>
      </Card>
    </Link>
  );
}
