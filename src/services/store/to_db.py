import os
import pandas as pd
import pymongo

from src.grpc_.services_pb2 import ComponentMessage, ComponentResponse
from src.grpc_.services_pb2_grpc import ComponentServicer, ComponentStub
from src.grpc_.utils import start_server

from icecream import ic
ic.configureOutput(includeContext=False)

class StoreDB(ComponentServicer):
    def __init__(self, host, port, user, name) -> None:
        self.host = host
        self.port = port
        self.user = user
        self.name = name
        self.output_file = file_name
        ic(f"Started on {os.environ.get('PORT')}")

    def forward(self, msg: ComponentMessage, context) -> ComponentResponse:
        if msg.health_check:
            ic("Health check")
            return ComponentResponse(output=msg.input)

        ic("Started Mongo-client")
        client = MongoClient(f"mongodb://{USER}:{PASSWORD}@{HOST}:{PORT}/")
        ic("Created client at {HOST}:{PORT}")
        db = client["test_db"]
        collection = db["test_collection"]

        result = collection.insert_one({
            "name": "test",
            "value": 123
        })
        ic(f"Inserted document with _id: {result.inserted_id}")

        document = collection.find_one({"name": "test"})
        ic(f"Retrieved document: {document}")
        return collection
        return ComponentResponse(output=[0.])


if __name__ == "__main__":
    from src.services.mongo.mongo import USER, PASSWORD
    HOST = os.environ.get("HOST", "mongo")
    PORT = int(os.environ.get("TARGET_PORT", 27017))

    service = StoreDB(
        HOST, PORT, USER, PASSWORD
    )
    start_server(service, port=int(os.environ.get("PORT")))
