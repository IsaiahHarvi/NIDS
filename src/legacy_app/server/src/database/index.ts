import { MongoClient, Db } from "mongodb";
import * as pc from "picocolors";
// import { setupClientDb } from "./setup-databases";

// const MONGO_URL = "mongodb://root:example@localhost:27017/?authSource=admin";
const MONGO_URL =
  process.env.WEBSERVER_MONGO_URL || "mongodb://root:example@mongo:27017/";

let client: MongoClient;
export let clientDb: Db;
export let componentsDb: Db;
export let storeServiceDb: Db;
export let reportsDb: Db;
// export let offlineFeederReports: Db;
//may need to play with making this async again,
//removed async because of bug where it sends multiple CS messages
const connectToDatabase = () => {
  try {
    client = new MongoClient(MONGO_URL, {
      connectTimeoutMS: 30000,
    });
    client.connect();
    storeServiceDb = client.db("services");
    reportsDb = client.db("reports");

    // setupClientDb(clientDb);
    console.log(pc.green("Success: MongoDB Connected"));
  } catch (error) {
    console.log(pc.red("Error: MongoDB Connection Failed"), error);
  }
};

export const initializeDatabase = async () => {
  await connectToDatabase();
};
