"""
Simple method to interact with the gRPC services oustide of the test suite.
"""

import click
import grpc

from icecream import ic

from src.grpc_.types import ComponentMessage
from src.grpc_.services_pb2_grpc import ComponentStub


@click.command()
@click.option("--port", default=50054, help="Port of the service to connect to.")
@click.option("--interactive", "-i", is_flag=True, default=False)
def main(port: int, interactive: bool) -> None:
    if interactive:
        while True:
            connect(port=int(input("PORT: ")))
    else:
        connect(port)


def connect(port: int) -> None:
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
                stub = ComponentStub(channel)
                request = ComponentMessage(input=[float(i) for i in range(100)], health_check=False)
                response = stub.forward(request)
                ic(response.output)
        case _:
            with grpc.insecure_channel(f"localhost:{port}") as channel:
                stub = ComponentStub(channel)
                request = ComponentMessage(input=[0.0], health_check=True)
                response = stub.forward(request)
                ic(response.output)


if __name__ == "__main__":
    main()
