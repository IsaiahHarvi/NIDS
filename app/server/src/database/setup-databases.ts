import type { Db } from "mongodb";
import { templateAttack } from "../lib/template-attack";
export async function setupClientDb(db: Db) {
  // create collections
  await db.createCollection("current_attack");
  await db.createCollection("saved_attacks");

  const savedAttacks = db.collection("saved_attacks");

  if (!(await savedAttacks.findOne({ name: templateAttack.name }))) {
    await savedAttacks.insertOne(templateAttack);
  }
}
