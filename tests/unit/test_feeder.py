import grpc
import os
import pytest
import multiprocessing
import time
from icecream import ic
from src.grpc_.utils import start_server
from src.grpc_.services_pb2 import ComponentMessage, ComponentResponse
from src.grpc_.services_pb2_grpc import ComponentStub
from tests.conftest import compose

from src.services.feeder.feeder import Feeder

from src.ai.DataModule import DataModule
@pytest.mark.skip("feeder disconnects")
def test_model():
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
