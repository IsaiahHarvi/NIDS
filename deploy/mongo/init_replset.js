try {
  sleep(8000); // Wait for MongoDB to be ready
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

  if (result.ok) {
    print("REPLICA SET INITIALIZED SUCCESSFULLY!");
    printjson(result);

    sleep(4000); // pls
    sleep(4000); // pretty pls

    print("Creating user...");
    const adminDb = db.getSiblingDB("admin");
    adminDb.createUser({
      user: "root",
      pwd: "example",
      roles: [{ role: "root", db: "admin" }]
    });
    print("USER CREATED SUCCESSFULLY!");
  } else {
    print("Failed to initialize replica set:");
    printjson(result);
  }
} catch (e) {
  print("ERROR INITIALIZING REPLICA SET OR CREATING USER:");
  printjson(e);
}
