try {
  sleep(8000);
  print("INITIALIZING REPLICA SET...");

  const result = rs.initiate({
    _id: "rs0",
    members: [
      {
        _id: 0,
        host: "mongo:27017",
      },
    ],
  });
  print("REPLICA SET INITIALIZED SUCCESSFULLY!");
  printjson(result);

  sleep(4000);
  sleep(4000);

  adminDb.createUser({
    user: "root",
    pwd: "example",
    roles: [{ role: "root", db: "admin" }]
  });

  print("init script compleeted");

  print("USER CREATED SUCCESSFULLY!");
} catch (e) {
  print("ERROR INITIALIZING REPLICA SET:");
  printjson(e);
}
