import { Elysia } from "elysia";
import { swagger } from "@elysiajs/swagger";
import { cors } from "@elysiajs/cors";
import { staticPlugin } from "@elysiajs/static";

const app = new Elysia()
  .use(cors())
  .use(swagger())
  .get("/", () => "Hello Elysia")
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
  .listen(3000);

console.log(
  `🦊 Elysia is running at ${app.server?.hostname}:${app.server?.port}`
);
