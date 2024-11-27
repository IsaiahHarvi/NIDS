import { useState } from "react";
import { Link } from "@tanstack/react-router";
import {
  Home,
  Sparkles,
  Crosshair,
  ScrollText,
  Gamepad2,
  HelpCircle,
  Settings,
  Clipboard,
} from "lucide-react";
import type { LucideIcon } from "lucide-react";
import { Tooltip, TooltipContent, TooltipTrigger } from "./ui/tooltip";
import { cn } from "@/lib/utils";
import SettingsModal from "./settingsModal"; // Import the SettingsModal component

interface LinkItemProps {
  to: string;
  icon: LucideIcon;
  label: string;
  pathCheck: string;
  disabled?: boolean;
}

function LinkItem({
  to,
  icon: Icon,
  label,
  pathCheck,
  disabled = false,
}: LinkItemProps) {
  return (
    <Tooltip>
      <TooltipTrigger asChild>
        <Link
          to={to}
          className="flex h-9 w-full text-muted-foreground transition-colors hover:text-primary"
          activeProps={{ className: "text-primary" }}
          disabled={disabled}
        >
          <div
            className={cn(
              "h-full w-[2px] left-0 top-0 bottom-0",
              location.pathname === pathCheck ? "bg-current" : "bg-background"
            )}
          />
          <Icon className="h-5 w-12 m-auto text-inherit" />
          <span className="sr-only">{label}</span>
        </Link>
      </TooltipTrigger>
      <TooltipContent side="right">{label}</TooltipContent>
    </Tooltip>
  );
}

function BottomLinkItem({
  to,
  icon: Icon,
  label,
  pathCheck,
  disabled = false,
}: LinkItemProps) {
  return (
    <Tooltip>
      <TooltipTrigger asChild>
        <Link
          to={to}
          className="flex h-9 w-full text-muted-foreground transition-colors hover:text-primary"
          activeProps={{ className: "text-primary" }}
          disabled={disabled}
        >
          <div
            className={cn(
              "h-full w-[3px] left-0 top-0 bottom-0",
              location.pathname === pathCheck ? "bg-current" : "bg-background"
            )}
          />
          <Icon className="h-5 w-8 m-auto text-inherit" />
          <span className="sr-only">{label}</span>
        </Link>
      </TooltipTrigger>
      <TooltipContent side="right">{label}</TooltipContent>
    </Tooltip>
  );
}

export function Navbar(): JSX.Element {
  const [isSettingsModalOpen, setSettingsModalOpen] = useState(false); // State to control modal

  const openSettingsModal = () => setSettingsModalOpen(true);
  const closeSettingsModal = () => setSettingsModalOpen(false);

  return (
    <aside className="inset-y fixed left-0 z-20 flex h-full flex-col  bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <nav className="flex flex-col items-center gap-4 py-2">
        <LinkItem to="/" icon={Home} label="Home" pathCheck="/" />
        <LinkItem
          to="/help"
          icon={Gamepad2}
          label="Controls"
          pathCheck="/help"
        />
        <LinkItem
          to="/logs"
          icon={ScrollText}
          label="Log Page"
          pathCheck="/logs"
        />
        <LinkItem
          to="/attack-control"
          icon={Crosshair}
          label="Attack Control"
          pathCheck="/attack-control"
        />
        <LinkItem
          to="/reports"
          icon={Sparkles}
          label="Reports"
          pathCheck="/reports"
        />
        <LinkItem
          to="/dashboard"
          icon={Clipboard}
          label="Dashboard"
          pathCheck="/dashboard"
        />
      </nav>
      <nav className="mt-auto grid gap-1 p-2">
        <BottomLinkItem
          to="/help"
          icon={HelpCircle}
          label="Help"
          pathCheck="/help"
        />
        {/* When clicking on this icon, open the SettingsModal */}
        <Tooltip>
          <TooltipTrigger asChild>
            <button
              onClick={openSettingsModal}
              className="flex h-9 w-full text-muted-foreground transition-colors hover:text-primary"
            >
              <div className="h-full w-[3px] left-0 top-0 bottom-0 bg-background" />
              <Settings className="h-5 w-8 m-auto text-inherit" />
              <span className="sr-only">Settings</span>
            </button>
          </TooltipTrigger>
          <TooltipContent side="right">Settings</TooltipContent>
        </Tooltip>
      </nav>

      {/* Render SettingsModal if the state is open */}
      {isSettingsModalOpen && (
        <SettingsModal
          isOpen={isSettingsModalOpen}
          onClose={closeSettingsModal}
        />
      )}
    </aside>
  );
}
