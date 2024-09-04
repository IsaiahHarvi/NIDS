"""
Simple method to interact with the gRPC services oustide of the test suite.
"""

import time
import click
import grpc
import numpy as np
from icecream import ic

from src.grpc_.services_pb2 import ComponentMessage
from src.grpc_.services_pb2_grpc import ComponentStub


@click.command()
@click.option("--port", default=50054, help="Port of the service to connect to.")
@click.option(
    "--interactive",
    "-i",
    is_flag=True,
    default=False,
    help="Pass in ports interactively.",
)
@click.option(
    "--live",
    "-l",
    is_flag=True,
    default=False,
    help="Continue to generate samples for services that support it.",
)
@click.option(
    "--sleep",
    "-s",
    default=7,
    help="Time to sleep between requests when running in live mode.",
)
def main(port: int, interactive: bool, live: bool, sleep: int) -> None:
    if interactive:
        while True:
            connect(port=int(input("PORT: ")), live=False)
    else:
        connect(port, live, sleep)


def connect(port: int, live: bool, sleep: int = 7) -> None:
    match port:
        case 50052:
            # Connect to Neural Network Service
            with grpc.insecure_channel(f"localhost:{port}") as channel:
                stub = ComponentStub(channel)
                request = ComponentMessage(input=[1.0, 2.0, 3.0], health_check=True)
                response = stub.forward(request)
                ic(response.output)
        case 50053 | 50054 | 50055:
            # Connect to Feeder, Offline-Feeder, or Logger
            with grpc.insecure_channel(f"localhost:{port}") as channel:
                stub = ComponentStub(channel)
                request = ComponentMessage(input=[], prediction=-1)
                response = stub.forward(request)
                ic(response.output)
        case 50056 | 50057:
            # Connect to Store-DB or Store-File
            with grpc.insecure_channel(f"localhost:{port}") as channel:
                while True:
                    stub = ComponentStub(channel)
                    request = ComponentMessage(
                        input=[np.random.uniform(1, 9000) for _ in range(80)],
                        prediction=-1
                    )
                    response = stub.forward(request)
                    # ic(response.output)
                    if not live:
                        break
                    time.sleep(sleep)

        case _:
            with grpc.insecure_channel(f"localhost:{port}") as channel:
                stub = ComponentStub(channel)
                request = ComponentMessage(input=[0.0], health_check=True)
                response = stub.forward(request)
                ic(response.output)


if __name__ == "__main__":
    main()
