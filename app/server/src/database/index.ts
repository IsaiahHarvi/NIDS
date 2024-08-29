// @/database/: Contains database initialization and Prisma clients
import { MongoClient, Db } from "mongodb";
import * as pc from "picocolors";
import { setupClientDb } from "./setup-databases";

// Updated MongoDB URL
// const MONGO_URL =
//   "mongodb://root:pass@host.docker.internal:27017/?authSource=admin";

// const MONGO_URL = "mongodb://root:example@localhost:27017/?authSource=admin";

//original
// const MONGO_URL = "mongodb://root:pass@mongo:27017/";
//new
const MONGO_URL = "mongodb://root:pass@host.docker.internal:27017/";

let client: MongoClient;
export let clientDb: Db;
export let componentsDb: Db;

const connectToDatabase = async () => {
  try {
    client = new MongoClient(MONGO_URL);
    await client.connect();

    clientDb = client.db("client");
    componentsDb = client.db("components");

    setupClientDb(clientDb);
    console.log(pc.green("Success: MongoDB Connected"));
  } catch (error) {
    console.log(pc.red("Error: MongoDB Connection Failed"), error);
  }
};

export const initializeDatabase = async () => {
  await connectToDatabase();
};
