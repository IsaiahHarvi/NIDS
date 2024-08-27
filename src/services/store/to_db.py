import os
import numpy as np
from pymongo import MongoClient

from src.grpc_.services_pb2 import ComponentMessage, ComponentResponse
from src.grpc_.services_pb2_grpc import ComponentServicer, ComponentStub
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

    def forward(self, msg: ComponentMessage, context) -> ComponentResponse:
        if msg.health_check:
            ic("Health check")
            return ComponentResponse(output=msg.input)

        try:
            client = MongoClient(f"mongodb://{self.user}:{self.password}@{self.host}:{self.port}/")
            ic(f"Created client at {self.host}:{self.port}")
            db = client["store_service"]
            collection = db["default"]

            result = collection.insert_one({
                "input": list(msg.input)
            })
            ic(result.inserted_id)
        except Exception as e:
            ic(e)
            return ComponentResponse(output=[1.])

        return ComponentResponse(output=[0.])


if __name__ == "__main__":
    from src.services.mongo.mongo import USER, PASSWORD
    HOST = os.environ.get("HOST", "mongo")
    PORT = int(os.environ.get("TARGET_PORT", 27017))

    service = StoreDB(
        HOST, PORT, USER, PASSWORD
    )
    start_server(service, port=int(os.environ.get("PORT", 50057)))
