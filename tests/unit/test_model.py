import grpc
import os
import pytest
import multiprocessing
import time
from icecream import ic
from src.grpc_.utils import start_server
from src.grpc_.services_pb2 import ComponentMessage, ComponentResponse
from src.grpc_.services_pb2_grpc import ComponentStub

from src.services.model.model import NeuralNetwork

from src.ai.DataModule import DataModule


@pytest.fixture(scope="module")
def grpc_server():
    os.system("docker kill $(docker ps -q) > /dev/null 2>&1")
    os.system("docker container prune -f > /dev/null 2>&1")
    os.system("docker image prune -f > /dev/null 2>&1")

    server_process = multiprocessing.Process(
        target=start_server,
        args=(NeuralNetwork("data/checkpoints/ResidualSmall.ckpt"), 50052),
    )
    server_process.start()
    time.sleep(1)
    yield
    server_process.terminate()
    server_process.join()


@pytest.mark.order(-1)  # run this last becuase its aggressive w/ containers
def test_model(grpc_server):
    try:
        with grpc.insecure_channel("localhost:50052") as channel:
            stub = ComponentStub(channel)
            dm = DataModule(
                paths=[f"data/CIC/test_data.csv"],
                batch_size=1,
                num_workers=1
            )
            dm.setup()

            data, label = next(iter(dm.train_dataloader()))
            data = data.numpy().flatten().tolist()  # [80] bc it has to live over gRPC

            msg = ComponentMessage(flow=data)
            response = stub.forward(msg)
            assert isinstance(response, ComponentResponse)
            ic(f"Got {response.prediction}, expected {label.item()}")
    except Exception as e:
        ic(e)
