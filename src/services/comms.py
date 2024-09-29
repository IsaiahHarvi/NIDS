# !/usr/bin/env python3

import time
import click
import grpc
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
@click.option("--test", is_flag=True, default=False)
def main(port: int, interactive: bool, live: bool, sleep: int, test: bool) -> None:
    if interactive:
        while True:
            connect(port=int(input("PORT: ")), live=False)
    elif test:
        for i in range(
            50053, 50057
        ):  # skip 50052 because we have a dedicated test for it
            time.sleep(3)
            ic(f"Testing Service on port {i}")
            connect(port=i, live=False)
    else:
        connect(port, live, sleep)


def connect(port: int, live: bool, sleep: int = 7) -> None:
    options = [
        ("grpc.max_send_message_length", 50 * 1024 * 1024),  # 50 MB
        ("grpc.max_receive_message_length", 50 * 1024 * 1024),  # 50 MB
    ]
    try:
        match port:
            case 50053 | 50054:
                # Connect to Feeder, Offline-Feeder
                with grpc.insecure_channel(
                    f"localhost:{port}", options=options
                ) as channel:
                    while True:
                        stub = ComponentStub(channel)
                        response = stub.forward(ComponentMessage())
                        # ic(response)
                        if not live:
                            break
            case 50055:
                # This is the logger service.
                pass
            case 50056 | 50057:
                # Connect to Store-DB or Store-File
                with grpc.insecure_channel(
                    f"localhost:{port}", options=options
                ) as channel:
                    from numpy import random

                    while True:
                        stub = ComponentStub(channel)
                        request = ComponentMessage(
                            flow=[random.uniform(1, 9000) for _ in range(80)],
                        )
                        response = stub.forward(request)
                        # ic(response.flow)
                        if not live:
                            break
                        time.sleep(sleep)
            case _:
                with grpc.insecure_channel(
                    f"localhost:{port}", options=options
                ) as channel:
                    stub = ComponentStub(channel)
                    request = ComponentMessage(flow=[1.0, 2.0, 3.0], health_check=True)
                    response = stub.forward(request)
                    assert response.return_code == 0
    except grpc.RpcError as e:
        if e.code() == grpc.StatusCode.UNAVAILABLE:  # pylint: disable=E1101
            ic(f"Server at {port} is unavailable. Is it running?")
        else:
            ic("Error", e)


if __name__ == "__main__":
    main()
