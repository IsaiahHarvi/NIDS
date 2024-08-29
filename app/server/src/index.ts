import { Elysia } from "elysia";
import { swagger } from "@elysiajs/swagger";
import { cors } from "@elysiajs/cors";
import { staticPlugin } from "@elysiajs/static";
import { initializeDatabase } from "./database";
import { ClientRoutes } from "./routes/clientRoutes";

async function startServer() {
  await initializeDatabase();

  const app = new Elysia()
    .use(cors())
    .use(swagger())
    .get("/", () => "Hello Elysia")
    .get("/ping", () => ({ message: "pong" }))
    .post("/hello", () => "world")
    .use(
      staticPlugin({
        prefix: "/",
        alwaysStatic: true,
        assets: "dist",
      })
    )
    .get("*", async () => {
      return Bun.file("./dist/index.html");
    })
    //this is where you will use the routes from different files
    .use(ClientRoutes)
    .listen(3000);

  console.log(
    `🦊 Elysia is running at ${app.server?.hostname}:${app.server?.port}`
  );

  return app;
}

export const app = await startServer();
