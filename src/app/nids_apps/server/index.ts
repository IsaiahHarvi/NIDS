import { Elysia } from "elysia";
import { PrismaClient } from "@prisma/client";

// const prisma = new PrismaClient();
const app = new Elysia();

app.get("/", () => "Hello from Elysia!");

app.get("/users", async () => {
  // return await prisma.user.findMany();
  return [];
});

app.listen(3000, () => {
  console.log("Server running at http://localhost:3000");
});
