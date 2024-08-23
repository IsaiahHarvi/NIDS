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

        data = next(iter(dm.train_dataloader()))[0]
        if data.dim() == 3:
            data = data.squeeze(0) 

        data = data.numpy()
        msg = ComponentMessage(input=data)
        ic(dm.train_dataset[0][0].shape)

        response = stub.forward(msg)
        assert isinstance(response, ComponentResponse)
        ic(response.output)