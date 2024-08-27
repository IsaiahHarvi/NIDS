import grpc
import os
import pytest
import multiprocessing
import time
import numpy as np
from icecream import ic
from src.grpc_.utils import start_server
from src.grpc_.services_pb2 import ComponentMessage, ComponentResponse
from src.grpc_.services_pb2_grpc import ComponentStub

from src.services.model.recurrent import RecurrentModel
from src.services.model.residual import ResidualModel

from src.ai.DataModule import DataModule


@pytest.fixture(scope="module")
def grpc_server(request):
    os.system("docker kill $(docker ps -q) > /dev/null 2>&1")
    os.system("docker container prune -f > /dev/null 2>&1")
    os.system("docker image prune -f > /dev/null 2>&1")

    model_class, port = request.param
    server_process = multiprocessing.Process(
        target=start_server, args=(model_class(), port)
    )
    server_process.start()
    time.sleep(1)
    yield port
    server_process.terminate()
    server_process.join()


@pytest.mark.parametrize(
    "grpc_server", [(RecurrentModel, 50051), (ResidualModel, 50052)], indirect=True
)
def test_model(grpc_server):
    try:
        port = grpc_server
        with grpc.insecure_channel(f"localhost:{port}") as channel:
            stub = ComponentStub(channel)
            dm = DataModule(
                paths=[f"data/CIC/Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv"],
                batch_size=1,
            )
            dm.setup()

            data, label = next(iter(dm.train_dataloader()))
            data = data.numpy().flatten().tolist()  # [80] bc it has to live over gRPC
            msg = ComponentMessage(input=data)

            response = stub.forward(msg)
            assert isinstance(response, ComponentResponse)
            ic(f"Got {response.prediction}, expected {label.item()}")
    except Exception as e:
        ic(e)
