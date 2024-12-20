import os

import pytest
from icecream import ic
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

from src.grpc_.utils import wait_for_services


@pytest.fixture(scope="session", autouse=True)
def mongo_compose():
    os.system("docker compose up --build -d")
    wait_for_services(["mongo", "mongo-express"], timeout=10, init_time=5)
    yield
    os.system("docker compose down")


@pytest.mark.skip("The Replica Set deprecated this test")
def test_mongo(mongo_compose):
    host = os.environ.get("host", "localhost")
    port = int(os.environ.get("port", 27017))

    ic(f"Attempting to connect to MongoDB at {host}:{port}")

    try:
        client = MongoClient(
            f"mongodb://root:example@{host}:{port}/", serverSelectionTimeoutMS=5000
        )
        client.server_info()  # Will raise an exception if unable to connect
        ic("Successfully connected to MongoDB")
    except ConnectionFailure as e:
        pytest.fail(f"Failed to connect to MongoDB: {str(e)}")

    db = client["test_db"]
    collection = db["test_collection"]

    result = collection.insert_one({"name": "test", "value": "Hello World!"})
    ic(f"Inserted document with _id: {result.inserted_id}")

    document = collection.find_one({"name": "test"})
    assert document, "Document not found in collection"

    client.close()
