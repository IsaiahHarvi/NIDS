import os
import pytest
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from icecream import ic
from src.grpc_.utils import wait_for_services


@pytest.fixture(scope="session", autouse=True)
def setup_mongo():
    os.system("docker compose -f deploy/mongo/compose.yml up --build -d")
    wait_for_services(["mongo", "mongo-express"], timeout=10, init_time=5)
    yield
    os.system("docker compose -f deploy/mongo/compose.yml down")


@pytest.mark.slow
def test_mongo():
    host = os.environ.get("host", "localhost")
    port = int(os.environ.get("port", 27017))
    # user = os.environ.get("user", "root")
    # password = os.environ.get("password", "example")

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
