try {
  var config = {
    _id: "rs0",
    members: [
      {
        _id: 0,
        host: "mongo:27017",
      },
    ],
  };
  var result = rs.initiate(config);
  printjson(result);

  // If the initiation fails, try to force reconfig
  if (result.ok !== 1) {
    print("Initiation failed, forcing config.");
    result = rs.reconfig(config, { force: true });
    printjson(result);
  }

  sleep(5000);
  adminDb = db.getSiblingDB("admin");
  adminDb.createUser({
    user: "root",
    pwd: "pass",
    roles: ["root"],
  });
} catch (e) {
  print("ERROR:");
  printjson(e);
}
