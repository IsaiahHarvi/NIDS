// imports etc
import { ModeToggle } from "./mode-toggle";

export function Topbar() {
  return (
    <header className="sticky top-0 z-10 flex h-14 items-center px-4 bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <h1 className="text-xl font-bold italic flex-1 text-center">
        NIDS - Network Intrusion Detection System
      </h1>
      <div className="flex items-center space-x-2">
        <nav className="flex items-center space-x-4">
          <ModeToggle />
        </nav>
      </div>
    </header>
  );
}
