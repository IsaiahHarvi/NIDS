import os

import icecream as ic
import numpy as np
import pandas as pd

from src.grpc_.services_pb2 import ComponentMessage, ComponentResponse
from src.grpc_.services_pb2_grpc import ComponentServicer
from src.grpc_.utils import start_server


class Example(ComponentServicer):
    def __init__(self):
        ic(f"Started on {os.environ.get('PORT')}")

    def forward(self, msg: ComponentMessage, context) -> ComponentResponse:
        if msg.health_check:
            ic("Health check")
            return ComponentResponse(return_code=0)

        return ComponentResponse(return_code=0)


if __name__ == "__main__":
    arg1 = os.environ.get("arg1", "default")
    service = Example(arg1)
    start_server(service, port=int(os.environ.get("PORT")))
