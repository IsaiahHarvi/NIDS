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
from src.services.model.residual import ResidualModel

from src.ai.DataModule import DataModule

@pytest.fixture(scope="module")
def grpc_server(request):
    model_class, port = request.param
    server_process = multiprocessing.Process(target=start_server, args=(model_class(), port))
    server_process.start()
    time.sleep(1)
    yield port
    server_process.terminate()
    server_process.join()

@pytest.mark.parametrize("grpc_server", [(RecurrentModel, 50051), (ResidualModel, 50052)], indirect=True)
def test_model(grpc_server):
    port = grpc_server
    with grpc.insecure_channel(f'localhost:{port}') as channel:
        stub = ComponentStub(channel)
        dm = DataModule(
            paths=[
                f"data/CIC/Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv"   
            ],
            batch_size=1, 
        )
        dm.setup()

        data, label = next(iter(dm.train_dataloader()))

        data = data.numpy().flatten().tolist() # [80] bc it has to live over gRPC
        msg = ComponentMessage(input=data)

        response = stub.forward(msg)
        assert isinstance(response, ComponentResponse)
        assert response.output == label.item(), f"False Prediction, expected {label.item()} but got {response.output}"

if __name__ == "__main__":
    pytest.main(["-sv", "tests/unit/test_model.py"])
