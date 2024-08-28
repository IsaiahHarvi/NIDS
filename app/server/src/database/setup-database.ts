import type { Db } from "mongodb";
// import { manyVsuts } from "@/lib/template-toels/many-vsuts";
// import { newToel } from "@/lib/template-toels/new-toel";
// import { vSutSimple, missionA, missionB } from "@/lib/template-missions";

export async function setupClientDb(db: Db) {
  // create collections
  // await db.createCollection("saved_toels");
  // await db.createCollection("saved_missions");
  await db.createCollection("current_toel");

  // Insert TOEL if one of the same name does not exist
  const templateToelsCollection = db.collection("template_toels");

  if (!(await templateToelsCollection.findOne({ name: manyVsuts.name }))) {
    await templateToelsCollection.insertOne(manyVsuts);
  }

  if (!(await templateToelsCollection.findOne({ name: newToel.name }))) {
    await templateToelsCollection.insertOne(newToel);
  }

  // Upsert saved missions
  const templateMissionsCollection = db.collection("template_missions");

  await templateMissionsCollection.updateOne(
    { name: vSutSimple.name },
    { $set: vSutSimple },
    { upsert: true }
  );
  await templateMissionsCollection.updateOne(
    { name: missionA.name },
    { $set: missionA },
    { upsert: true }
  );
  await templateMissionsCollection.updateOne(
    { name: missionB.name },
    { $set: missionB },
    { upsert: true }
  );
}
