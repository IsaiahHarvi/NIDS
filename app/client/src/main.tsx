import ReactDOM from "react-dom/client";
import { RouterProvider, createRouter } from "@tanstack/react-router";
import "./index.css";
// Import the generated route tree
import { routeTree } from "./routeTree.gen";
import { ThemeProvider } from "./components/theme-provider";
// import { TooltipProvider } from "./components/ui/tooltip";
// import { Topbar } from "./components/topbar";
// import { Navbar } from "./components/navbar";

// Create a new router instance
const router = createRouter({ routeTree });

// Register the router instance for type safety
declare module "@tanstack/react-router" {
  interface Register {
    router: typeof router;
  }
}
// Render the app
const rootElement = document.getElementById("root")!;
if (!rootElement.innerHTML) {
  const root = ReactDOM.createRoot(rootElement);
  root.render(
    <ThemeProvider defaultTheme="dark" storageKey="vite-ui-theme">
      <RouterProvider router={router} />
      {/* <WebSocketContextProvider> */}
      {/* <Navbar /> */}
      {/* <Topbar /> */}
      {/* <Toaster /> */}
      {/* <TailwindIndicator /> */}
      {/* </WebSocketContextProvider> */}
    </ThemeProvider>
  );
}
