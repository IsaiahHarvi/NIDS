import { Topbar } from "@/components/topbar";
import { createRootRoute, Outlet } from "@tanstack/react-router";
// import WebSocketContextProvider from "@/middleware/WebSocketContext";
import { Navbar } from "@/components/navbar";
import { Toaster } from "@/components/ui/toaster";
export const Route = createRootRoute({
  component: () => (
    <div className="bg-background text-foreground h-screen w-screen">
      <Topbar />
      <div className="flex pt-12 pl-14">
        <Navbar />
        <Outlet />
      </div>
      <Toaster />
    </div>
  ),
});
