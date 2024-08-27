import os
import pandas as pd
import pymongo

from src.grpc_.services_pb2 import ComponentMessage, ComponentResponse
from src.grpc_.services_pb2_grpc import ComponentServicer, ComponentStub
from src.grpc_.utils import start_server

from icecream import ic
ic.configureOutput(includeContext=False)

class StoreDB(ComponentServicer):
    def __init__(self, file_name: str) -> None:
        self.output_file = file_name
        ic(f"Started on {os.environ.get('PORT')}")

    def forward(self, msg: ComponentMessage, context) -> ComponentResponse:
        if msg.health_check:
            ic("Health check")
            return ComponentResponse(output=msg.input)

        return ComponentResponse(output=[0.])


if __name__ == "__main__":
    from src.services.mongo.mongo import USER, PASSWORD

    HOST = os.environ.get("HOST", "localhost")
    PORT = int(os.environ.get("TARGET_PORT", 27017))

    service = StoreDB(
        HOST, PORT, USER, PASSWORD
    )
    start_server(service, port=int(os.environ.get("PORT")))
