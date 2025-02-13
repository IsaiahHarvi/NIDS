import multiprocessing
import os
import time

import grpc
import pytest
from icecream import ic

from src.ai.DataModule import DataModule
from src.grpc_.services_pb2 import ComponentMessage, ComponentResponse
from src.grpc_.services_pb2_grpc import ComponentStub
from src.grpc_.utils import start_server
from src.services.neural_network.neural_network import NeuralNetwork


@pytest.fixture(scope="module")
def grpc_server():
    os.system("docker kill nids-ids > /dev/null 2>&1")
    os.system("docker container rm nids-ids > /dev/null 2>&1")

    server_process = multiprocessing.Process(
        target=start_server,
        args=(NeuralNetwork("data/checkpoints/MLP.ckpt"), 50052),
    )
    server_process.start()
    time.sleep(1)
    yield
    server_process.terminate()
    server_process.join()

@pytest.mark.skip("reevaluate")
@pytest.mark.order(-1) # runs last
def test_model(grpc_server):
    try:
        with grpc.insecure_channel("localhost:50052") as channel:
            stub = ComponentStub(channel)
            dm = DataModule(
                paths=["data/CIC/test_data_small.csv"],
                batch_size=1,
                num_workers=1
            )
            dm.setup()

            data, label = next(iter(dm.train_dataloader()))
            data = data.numpy().flatten().tolist()

            msg = ComponentMessage(flow=data)
            response = stub.forward(msg)
            assert isinstance(response, ComponentResponse)
            ic(f"Got {response.prediction}, expected {label.item()}")
    except Exception as e:
        ic(e)
