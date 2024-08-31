import { Topbar } from "@/components/topbar";
import { createRootRoute, Outlet } from "@tanstack/react-router";
import WebSocketContextProvider from "@/middleware/WebSocketContext";
import { Navbar } from "@/components/navbar";
import { TooltipProvider } from "@/components/ui/tooltip";
export const Route = createRootRoute({
  component: () => (
    <>
      <div className="p-2 flex gap-2">
        <TooltipProvider>
          <WebSocketContextProvider>
            <div className="grid h-screen max-h-screen w-full pl-[3.25rem] custom-scrollable-element bg-['/grid.svg']">
              <Navbar />
              <div className="flex flex-col flex-grow w-full bg-background">
                <Topbar />
                <div className="h-full dark:bg-[url('/grid.svg')] dark:bg-zinc-900/40 bg-zinc-100">
                  <Outlet />
                </div>
                {/* <Toaster /> */}
                {/* <TailwindIndicator /> */}
              </div>
            </div>
          </WebSocketContextProvider>
        </TooltipProvider>
      </div>
      <hr />
      {/* <TanStackRouterDevtools /> */}
    </>
  ),
});
