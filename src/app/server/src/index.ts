import { Elysia } from "elysia";
import { swagger } from "@elysiajs/swagger";
import { cors } from "@elysiajs/cors";
import { staticPlugin } from "@elysiajs/static";
import { initializeDatabase } from "./database";
import { websocketRoute, ServicesRoutes } from "./routes";
import path from "path";

async function startServer() {
  await initializeDatabase();

  const app = new Elysia()
    .use(swagger())
    .use(
      cors({
        origin: ({ headers }) => headers.get("origin") === "*",
        credentials: true,
      })
    )
    .use(
      staticPlugin({
        prefix: "/",  // Serve files from the root
        alwaysStatic: true,
        assets: path.resolve("/app/server/dist"),  // Full path to the dist folder
        })
    )
    // Fallback: Serve index.html for all non-static requests
    .get("^\\/(?!assets).*", async () => {
      return Bun.file(path.resolve("t/app/server/dist/index.html"));
    })
    .use(ServicesRoutes)
    .use(websocketRoute)
    .listen(8000);

  console.log(
    `Elysia is running at ${app.server?.hostname}:${app.server?.port}`
  );

  return app;
}

export const app = await startServer();
