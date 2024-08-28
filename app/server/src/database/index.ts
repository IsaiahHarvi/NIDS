// @/database/: Contains database initialization and Prisma clients
import { MongoClient, Db } from "mongodb";
import * as pc from "picocolors";
// import { setupClientDb } from "./setup-databases";

// this is sometimes needed
// const MONGO_URL = "mongodb://root:example@localhost:27017/?authSource=admin";
const MONGO_URL = "mongodb://root:pass@mongo:27017/";

let client: MongoClient;
export let clientDb: Db;
export let componentsDb: Db;
export let deployedDb: Db;
export let guiDb: Db;
export let logsDb: Db;
export let loggerComponentDb: Db;
export let missionDb: Db;
export let tbcfDb: Db;
export let testDb: Db;
export let vsutDb: Db;

const connectToDatabase = async () => {
  try {
    client = new MongoClient(MONGO_URL);
    await client.connect();

    clientDb = client.db("client");
    componentsDb = client.db("components");
    deployedDb = client.db("deploy-db");
    guiDb = client.db("gui");
    logsDb = client.db("logs");
    loggerComponentDb = client.db("logger_component");
    missionDb = client.db("mission-db");
    tbcfDb = client.db("tbcf");
    testDb = client.db("test");
    vsutDb = client.db("vsut");

    // setupClientDb(clientDb);
    console.log(pc.green("Success: MongoDB Connected"));
  } catch (error) {
    console.log(pc.red("Error: MongoDB Connection Failed"), error);
  }
};

export const initializeDatabase = async () => {
  await connectToDatabase();
};
