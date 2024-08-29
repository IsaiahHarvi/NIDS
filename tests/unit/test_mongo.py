import os
import pytest
import subprocess
import time
from pymongo import MongoClient
from icecream import ic

from src.grpc_.utils import wait_for_services

@pytest.fixture(scope="session", autouse=True)
def setup_mongo():
    os.system(
        "docker compose -f deploy/mongo/compose.yml up --build -d"
    )
    wait_for_services(["mongo", "mongo-express"], timeout=30, init_time=10)
    yield
    os.system(
        "docker compose -f deploy/mongo/compose.yml down"
    )

@pytest.mark.slow # the setup is slow but we have to mark here
@pytest.mark.skip("Not configured for testing quite yet")
def test_mongo():
    host = os.environ.get("host", "mongo")
    port = int(os.environ.get("port", 27017))
    user = os.environ.get("user", "root")
    password = os.environ.get("password", "pass")

    ic("Started Mongo-client")
    client = MongoClient(f"mongodb://{user}:{password}@{host}:{port}/")
    ic(f"Created client at {host}:{port}")
    db = client["test_db"]
    collection = db["test_collection"]

    result = collection.insert_one({
        "name": "test",
        "value": "Hello World!"
    })
    ic(f"Inserted document with _id: {result.inserted_id}")

    document = collection.find_one({"name": "test"})
    assert document, "Document not found in collection"
    return
