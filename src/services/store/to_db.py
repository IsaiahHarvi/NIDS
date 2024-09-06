import os
import numpy as np
from pymongo import MongoClient

from src.grpc_.services_pb2 import ComponentMessage, ComponentResponse
from src.grpc_.services_pb2_grpc import ComponentServicer
from src.grpc_.utils import start_server

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
            client = MongoClient(f"mongodb://root:example@mongo:27017/?replicaSet=rs0")
            db = client["store_service"]
            collection_name = (
                "default" if not msg.collection_name else msg.collection_name
            )
            collection = db[collection_name]
            result = collection.insert_one(
                {
                    "id_": msg.mongo_id,
                    "flow": list(msg.flow),
                    "prediction": int(msg.prediction) if msg.prediction else -1,
                }
            )
            ic(result.inserted_id, collection_name)
        except Exception as e:
            ic(e)
            return ComponentResponse(return_code=1)
        return ComponentResponse(return_code=0)


if __name__ == "__main__":
    service = StoreDB()
    start_server(service, port=os.environ.get("PORT"))
