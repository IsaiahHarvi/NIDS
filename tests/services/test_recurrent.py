import grpc
import pytest
import multiprocessing
import time
import numpy as np
from icecream import ic
from src.grpc.utils import start_server
from src.grpc.services_pb2 import ComponentMessage, ComponentResponse
from src.grpc.services_pb2_grpc import ComponentStub
from src.services.model.recurrent import RecurrentModel
from src.ai.DataModule import DataModule

@pytest.fixture(scope="module")
def grpc_server():
    server_process = multiprocessing.Process(target=start_server, args=(RecurrentModel(), 50051))
    server_process.start()
    time.sleep(1)
    yield
    server_process.terminate()
    server_process.join()

def test_recurrent(grpc_server):
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = ComponentStub(channel)
        dm = DataModule(
            paths=[
                # f"data/CIC/Thursday-WorkingHours-Afternoon-Infilteration.pcap_ISCX.csv",
                f"data/CIC/Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv"   
            ],
            batch_size=1, 
        )
        dm.setup()

        data, label = next(iter(dm.train_dataloader()))

        # ic(data.shape) # [1, 1, 80]
        data = data.numpy().flatten().tolist() # [80] bc it has to live over gRPC
        msg = ComponentMessage(input=data)

        response = stub.forward(msg)
        assert isinstance(response, ComponentResponse)
        # ic(response.output)
        assert response.output == label.item(), f"False Prediction, expected {label.item()} but got {response.output}"
