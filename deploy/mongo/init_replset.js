print("starting mongo init");

try {
  print("init replica set");

  // Initialize the replica set
  const result = rs.initiate({
    _id: "rs0",
    members: [
      {
        _id: 0,
        host: "mongo:27017",
      },
    ],
  });

  printjson(result);

  sleep(4000);
  sleep(4000);
  const adminDb = db.getSiblingDB("admin");
  adminDb.createUser({
    user: "test",
    pwd: "test",
    roles: [{ role: "root", db: "admin" }],
  });

  adminDb.createUser({
    user: "root",
    pwd: "example",
    roles: ["root"],
  });

  print("init script compleeted");

  print("USER CREATED SUCCESSFULLY!");
} catch (e) {
  print("ERROR INITIALIZING REPLICA SET:");
  printjson(e);
}

// try {
//   var config = {
//     _id: "rs0",
//     members: [
//       {
//         _id: 0,
//         host: "mongo:27017",
//       },
//     ],
//   };
//   var result = rs.initiate(config);
//   printjson(result);

//   // If the initiation fails, try to force reconfig
//   if (result.ok !== 1) {
//     print("Initiation failed, forcing config.");
//     result = rs.reconfig(config, { force: true });
//     printjson(result);
//   }

//   sleep(5000);
//   adminDb = db.getSiblingDB("admin");
//   adminDb.createUser({
//     user: "root",
//     pwd: "pass",
//     roles: ["root"],
//   });
// } catch (e) {
//   print("ERROR:");
//   printjson(e);
// }
