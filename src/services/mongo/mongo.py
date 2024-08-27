import os
from pymongo import MongoClient
from icecream import ic

HOST = os.environ.get("HOST", "mongo")
PORT = int(os.environ.get("PORT", 27017))
USER = os.environ.get("USER", "root")
PASSWORD = os.environ.get("PASSWORD", "pass")

def mongo_client(user=HOST, password=PASSWORD, host=HOST, port=PORT):
    """
    This is basically just a test to make sure that we can connect to 
    the mongo service. But, because we actually have a (for now unused) mongo-client service,
    this will stay outside of the test dir .
    """
    ic("Started Mongo-client")
    client = MongoClient(f"mongodb://{USER}:{PASSWORD}@{HOST}:{PORT}/")
    ic("Created client at {HOST}:{PORT}")
    db = client["test_db"]
    collection = db["test_collection"]

    result = collection.insert_one({
        "name": "test",
        "value": "Hello World!"
    })
    ic(f"Inserted document with _id: {result.inserted_id}")

    document = collection.find_one({"name": "test"})
    ic(f"Retrieved document: {document}")
    return collection


if __name__ == "__main__":
    mongo_client()
