"""
Simple method to interact with the gRPC services oustide of the test suite.
"""

import click
import grpc
import numpy as np
import time
from icecream import ic

from src.grpc_.services_pb2 import ComponentMessage
from src.grpc_.services_pb2_grpc import ComponentStub


@click.command()
@click.option("--port", default=50054, help="Port of the service to connect to.")
@click.option("--interactive", "-i", is_flag=True, default=False)
@click.option("--live", "-l", is_flag=True, default=False)
def main(port: int, interactive: bool, live: bool) -> None:
    if interactive:
        while True:
            connect(port=int(input("PORT: ")), live=False)
    else:
        connect(port, live)


def connect(port: int, live: bool) -> None:
    match port:
        case 50051 | 50052:
            # Connect to Model Services
            with grpc.insecure_channel(f"localhost:{port}") as channel:
                stub = ComponentStub(channel)
                request = ComponentMessage(input=[1.0, 2.0, 3.0], health_check=True)
                response = stub.forward(request)
                ic(response.output)
        case 50053 | 50054 | 50055:
            # Connect to Feeder or Logger Services
            with grpc.insecure_channel(f"localhost:{port}") as channel:
                stub = ComponentStub(channel)
                request = ComponentMessage(input=[])
                response = stub.forward(request)
                ic(response.output)
        case 50056 | 50057:
            # Connect to Store Services
            with grpc.insecure_channel(f"localhost:{port}") as channel:
                while True:
                    stub = ComponentStub(channel)
                    request = ComponentMessage(input=[np.random.uniform(1, 9000) for _ in range(80)])
                    response = stub.forward(request)
                    # ic(response.output)
                    if not live: break
                    time.sleep(3)

        case _:
            with grpc.insecure_channel(f"localhost:{port}") as channel:
                stub = ComponentStub(channel)
                request = ComponentMessage(input=[0.0], health_check=True)
                response = stub.forward(request)
                ic(response.output)


if __name__ == "__main__":
    main()
