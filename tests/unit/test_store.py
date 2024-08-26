"""
Sends the data from the offline feeder service to the store to file service.
For now, this is a unit test for both the offline feeder and the store-file service.
"""
import os
import pytest
import grpc
import threading
import pandas as pd
from time import sleep
from concurrent import futures
from icecream import ic

from src.grpc_.services_pb2 import ComponentMessage, ComponentResponse
from src.grpc_.services_pb2_grpc import add_ComponentServicer_to_server, ComponentStub
from src.grpc_.utils import start_server

from src.services.offline_feeder.offline_feeder import OfflineFeeder
from src.services.store.to_file import StoreFile


@pytest.fixture(scope="module")
def setup():
    store_service = StoreFile(file_name="offline_feeder.csv")
    store_server = start_server(store_service, 50056, wait_for_termination=False)
    store_thread = threading.Thread(target=store_server.wait_for_termination)
    store_thread.start()
    sleep(1)

    feeder_service = OfflineFeeder(p2p=True, host="localhost", target_port=50056)
    feeder_server = start_server(feeder_service, 50054, wait_for_termination=False)

    feeder_thread = threading.Thread(target=feeder_server.wait_for_termination)
    feeder_thread.start()
    sleep(1)

    yield

    # teardown
    store_server.stop(0)
    feeder_server.stop(0)
    store_thread.join()
    feeder_thread.join()

    if os.path.exists("offline_feeder.csv"):
        os.remove("offline_feeder.csv")
    
def test_store(setup):
    """
    Use the offline feeder to send data to the store to file service
    """
    try:
        with grpc.insecure_channel('localhost:50054') as channel:
            stub = ComponentStub(channel)
            response = stub.forward(
                ComponentMessage(input=[])
            )
            assert response.output == [0.], "The OfflineFeeder did not send data."
    except Exception as e:
        ic(e)
