import { createLazyFileRoute } from "@tanstack/react-router";
import {
  Card,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
// import Balancer from "react-wrap-balancer";
import type { LucideIcon } from "lucide-react";
import {
  Sparkles,
  Crosshair,
  ScrollText,
  Gamepad2,
  Clipboard,
} from "lucide-react";
import { Link } from "@tanstack/react-router";
// import logo from "@/components/logo/nids_logo.png";
// import "@/components/logo/logo.css";
export const Route = createLazyFileRoute("/")({
  component: Index,
});

export function Index() {
  return (
    <div className="container p-2">
      <div className="flex">
        <h3 className="text-4x1 font-black font-mono py-8 mx-auto tracking-widest">
          {" "}
          NIDS
        </h3>
      </div>
      {/* <div className="mt-12 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 w-full px-4 md:max-w-5xl">
        <LinkCard
          icon={Gamepad2}
          title="Help"
          description="NIDS Help Page"
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
          title="Test"
          description="Test page"
          link="/test"
        />
        <LinkCard
          icon={Sparkles}
          title="Reports"
          description="View Reports of NIDS"
          link="/reports"
        />
        <LinkCard
          icon={Clipboard}
          title="Dashboard"
          description="NIDS Dashboard"
          link="/dashboard"
        />
      </div> */}
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
      <Card className="hover:shadow-lg transition-shadow">
        <CardHeader>
          <CardTitle>
            <div className="flex items-center">
              <Icon className="h-8 w-8 text-primary mr-3" />
              <span className="text-lg font-semibold">{title}</span>
            </div>
          </CardTitle>
          <CardDescription>{description}</CardDescription>
        </CardHeader>
      </Card>
    </Link>
  );
}
