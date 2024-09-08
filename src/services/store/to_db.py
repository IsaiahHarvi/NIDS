import os
import numpy as np
from pymongo import MongoClient

from src.grpc_.services_pb2 import ComponentMessage, ComponentResponse
from src.grpc_.services_pb2_grpc import ComponentServicer
from src.grpc_.utils import start_server
from uuid import uuid4 as UUID

from icecream import ic

ic.configureOutput(includeContext=False)


class StoreDB(ComponentServicer):
    def __init__(self) -> None:
        ic(f"Started on {os.environ.get('PORT')}")

    def forward(self, msg: ComponentMessage, context=None) -> ComponentResponse:
        if msg.health_check:
            ic("Health check")
            return ComponentResponse(flow=msg.flow)

        try:
            client = MongoClient("mongodb://root:example@mongo:27017/?replicaSet=rs0")
            db = client["store_service"]
            collection = db["default"]
            result = collection.insert_one(
                {
                    "id_": str(UUID()),
                    "flow": list(msg.flow),
                }
            )
            ic(result.inserted_id)
        except Exception as e:
            ic(e)
            return ComponentResponse(return_code=1)
        return ComponentResponse(return_code=0)


if __name__ == "__main__":
    service = StoreDB()
    start_server(service, port=os.environ.get("PORT"))
