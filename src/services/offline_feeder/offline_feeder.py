import grpc
import os
import numpy as np
import pandas as pd

from src.grpc_.services_pb2 import ComponentMessage, ComponentResponse
from src.grpc_.services_pb2_grpc import ComponentServicer, ComponentStub
from src.grpc_.utils import start_server

from icecream import ic

ic.configureOutput(includeContext=False)


class OfflineFeeder(ComponentServicer):
    def __init__(self, p2p: bool, host, target_port) -> None:
        self.p2p = p2p
        self.host = host
        self.port = target_port
        ic(f"Started on {os.environ.get('PORT')}")

    def forward(self, msg: ComponentMessage, context) -> ComponentResponse:
        if msg.health_check:
            ic("Health check")
            return ComponentResponse(output=msg.input)

        df = pd.read_csv("data/CIC/Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv")
        df = df.select_dtypes(include=[np.number])
        df = df.drop(
            ["Flow_ID", "Source_IP", "Destination_IP", "Timestamp"],
            axis=1,
            errors="ignore",
        )
        df = df.select_dtypes(include=[float, int]).fillna(0)
        df.replace([np.inf, -np.inf], np.nan, inplace=True)
        df.fillna(df.mean(), inplace=True)

        sample = df.sample(n=1).iloc[0].to_numpy()
        data = sample.flatten()
        ic(data.shape)

        if self.p2p:
            self.send(data.tolist())
            return ComponentResponse(output=[0.0])

        return ComponentResponse(output=data.tolist())

    def send(self, data: list) -> None:
        with grpc.insecure_channel(f"{self.host}:{self.port}") as channel:
            stub = ComponentStub(channel)
            response = stub.forward(ComponentMessage(input=data))
            ic(response.output)
            ic(response.prediction)


if __name__ == "__main__":
    p2p: bool = os.environ.get("P2P", "true").lower() == "true"
    host = os.environ.get("HOST", "localhost")
    target_port = int(os.environ.get("TARGET_PORT", 50052))

    service = OfflineFeeder(p2p, host, target_port)
    start_server(service, port=int(os.environ.get("PORT")))
