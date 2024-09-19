import { createLazyFileRoute } from "@tanstack/react-router";
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
import logo from "@/assets/nids_logo.png";
import "@/assets/logo.css";

export const Route = createLazyFileRoute("/")({
  component: Index,
});

export function Index() {
  return (
    <div className="container mx-auto flex flex-col items-center justify-center py-12 px-4">
      <div className="flex flex-col items-center">
        <div className="logo-container mb-8">
          <img src={logo} alt="Logo" className="rotating-logo w-40 h-40" />
        </div>
        <div className="text-center">
          <h1 className="text-4xl font-bold leading-tight tracking-tighter md:text-5xl lg:leading-tight">
            NIDS
          </h1>
          <Balancer className="mt-4 max-w-[750px] text-lg font-light text-foreground">
            Network Intrusion Detection System
          </Balancer>
        </div>
      </div>
      <div className="mt-12 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 w-full px-4 md:max-w-5xl">
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
          title="Test"
          description="Test page"
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
