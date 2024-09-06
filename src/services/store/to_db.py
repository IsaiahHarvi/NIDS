import os
import numpy as np
from pymongo import MongoClient

from src.grpc_.services_pb2 import ComponentMessage, ComponentResponse
from src.grpc_.services_pb2_grpc import ComponentServicer
from src.grpc_.utils import start_server

from icecream import ic

ic.configureOutput(includeContext=False)


class StoreDB(ComponentServicer):
    def __init__(self, host, port, user, password) -> None:
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        ic(f"Started on {os.environ.get('PORT')}")

    def forward(self, msg: ComponentMessage | dict, context) -> ComponentResponse:
        if msg.health_check:
            ic("Health check")
            return ComponentResponse(output=msg.input)

        try:
            client = MongoClient(
                f"mongodb://{self.user}:{self.password}@{self.host}:{self.port}/?replicaSet=rs0"
                # f"mongodb://{self.host}:{self.port}/"
            )
            ic(f"Created client at {self.host}:{self.port}")
            db = client["store_service"]

            if isinstance(msg, ComponentMessage):
                collection_name = (
                    "default" if not msg.collection_name else msg.collection_name
                )
                collection = db[collection_name]
                result = collection.insert_one(
                    {
                        "id_": msg.mongo_id,
                        "input": list(msg.input),
                        "prediction": int(msg.prediction),
                    }
                )
                ic(result.inserted_id, collection_name)

            elif isinstance(msg, dict):
                collection = db[msg["collection_name"]]
                result = collection.insert_one(msg.remove("collection_name"))
                ic(result.inserted_id, collection_name)

        except Exception as e:
            ic(e)
            return ComponentResponse(output=[1.0])

        return ComponentResponse(output=[0.0])


if __name__ == "__main__":
    host = os.environ.get("HOST", "mongo")
    port = int(os.environ.get("TARGET_PORT", 27017))

    service = StoreDB(host, port, "root", "example")
    start_server(service, port=int(os.environ.get("PORT", 50057)))
