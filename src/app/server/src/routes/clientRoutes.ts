import { nanoid } from "nanoid";
import { Elysia } from "elysia";
import { clientDb } from "../database";
// Import Zod schemas here
import { Attack } from "../../../types/client-types";
import { AttackSchema } from "../lib/zod-schemas/client-schemas";

const parseData = (date: string | Date): Date => {
  return date instanceof Date ? date : new Date(date);
};

export const ClientRoutes = new Elysia().group("/api/client", (router) =>
  router
    .get("/saved_attacks", async () => {
      console.log("Getting saved attacks");
      return clientDb.collection("saved_attacks").find().toArray();
    })
    .get("/current_attack", async () => {
      return clientDb.collection("current_attack").findOne();
    })
    //possibly do it like this
    // .post("/current_attack", async ({body}) => {
    //     const attack: Attack = {
    //         ...body,
    //         attackId: nanoid(),
    //         startTime: parseData(body.startTime),
    //     };
    //     await clientDb.collection("current_attack").insertOne(attack);
    //     return attack;
    // })
    // .post("/current_attack", async (req) => {
    //   const attack: Attack = {
    //     ...req.body,
    //     attackId: nanoid(),
    //     startTime: parseData(req.body.startTime),
    //   };
    //   await clientDb.collection("current_attack").insertOne(attack);
    //   return attack;
    // })
    .put("/saved_attacks", async (req) => {
      const attack = req.body;
      const parse = AttackSchema.safeParse(attack);
      if (!parse.success) {
        console.error("Invalid attack data", parse.error);
        return new Response(
          JSON.stringify({
            error: "Invalid attack data",
            details: parse.error,
          }),
          { status: 400 }
        );
      }
      const validatedAttack = {
        ...parse.data,
        attackId: nanoid(),
        startTime: parseData(parse.data.startTime),
      };
      await clientDb.collection("saved_attacks").insertOne(validatedAttack);
      return new Response(JSON.stringify(validatedAttack), { status: 201 });
    })
    // .post("/saved_attacks", async (req) => {
    //   const attack: Attack = {
    //     ...req.body,
    //     attackId: nanoid(),
    //     startTime: parseData(req.body.startTime),
    //   };
    //   await clientDb.collection("saved_attacks").insertOne(attack);
    //   return attack;
    // })
    .delete("/saved_attacks/:attackId", async (req) => {
      const { attackId } = req.params;
      await clientDb.collection("saved_attacks").deleteOne({ attackId });
      return { attackId };
    })
    .delete("/current_attack", async () => {
      await clientDb.collection("current_attack").deleteOne({});
      return {};
    })
);
