import multiprocessing
import os
import time

import grpc
import pytest

from src.grpc_.services_pb2 import ComponentMessage, ComponentResponse
from src.grpc_.services_pb2_grpc import ComponentStub
from src.grpc_.utils import start_server
from services.feeder.feeder import Feeder


@pytest.mark.skip("feeder disconnects")
def test_feeder():
    server_process = multiprocessing.Process(
        target=start_server,
        args=(Feeder("eth0", "capture.pcap", 10), 50053),
    )
    server_process.start()
    time.sleep(1)

    with grpc.insecure_channel("localhost:50053") as channel:
        stub = ComponentStub(channel)

        msg = ComponentMessage(flow=[])
        response = stub.forward(msg)
        assert isinstance(response, ComponentResponse)

    server_process.terminate()
    server_process.join()
