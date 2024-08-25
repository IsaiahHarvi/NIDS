import grpc
import os
import numpy as np

from src.ai.DataModule import DataModule
from src.grpc_.services_pb2 import ComponentMessage, ComponentResponse
from src.grpc_.services_pb2_grpc import ComponentServicer, ComponentStub
from src.grpc_.utils import start_server

from icecream import ic
ic.configureOutput(includeContext=False)

class OfflineFeeder(ComponentServicer):
    def __init__(self, p2p: bool, host, port) -> None:
        self.p2p = p2p
        self.host = host
        self.port = port
        ic(f"Started on {os.environ.get('PORT')}")

    def forward(self, msg: ComponentMessage, context) -> ComponentResponse:
        if msg.health_check:
            ic("Health check")
            return ComponentResponse(output=msg.input)

        dm = DataModule(
            paths=[
                f"data/CIC/Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv"   
            ],
            batch_size=1, 
        )
        dm.setup()

        data, label = np.random.choice(list(dm.train_dataloader()))
        data = data.numpy().flatten().tolist() # [80] bc it has to live over gRPC

        if self.p2p:
            self.send_to_model(data)
            return ComponentResponse(output=[0.])

        return ComponentResponse(output=data)

    def send_to_model(self, data: list) -> None:
        with grpc.insecure_channel(f'{self.host}:{self.port}') as channel:
            stub = ComponentStub(channel)
            request = ComponentMessage(input=data)
            response = stub.forward(request)
            ic(f"Model Response: {response.output}")


if __name__ == "__main__":
    p2p:bool = os.environ.get("P2P", "true").lower() == "true"
    host = os.environ.get("HOST", "localhost")
    target_port = int(os.environ.get("TARGET_PORT", 50052))

    service = OfflineFeeder(p2p, host, target_port)
    start_server(service, port=int(os.environ.get("PORT")))
