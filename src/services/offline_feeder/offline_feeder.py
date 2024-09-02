import grpc
import os
import numpy as np
import pandas as pd

from src.grpc_.services_pb2 import ComponentMessage, ComponentResponse
from src.grpc_.services_pb2_grpc import ComponentServicer, ComponentStub
from src.grpc_.utils import start_server, send
from sklearn.preprocessing import MinMaxScaler

from icecream import ic

ic.configureOutput(includeContext=False)


class OfflineFeeder(ComponentServicer):
    def __init__(self, host, target_port) -> None:
        self.host = host
        self.port = target_port
        ic(f"Started on {os.environ.get('PORT')}")

    def forward(self, msg: ComponentMessage, context) -> ComponentResponse:
        if msg.health_check:
            ic("Health check")
            return ComponentResponse(output=msg.input)

        df = pd.read_csv("data/CIC/test_data.csv")
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

        x = MinMaxScaler().fit_transform(data).tolist()

        send(
            msg=ComponentMessage(input=x, collection_name=self.__class__.__name__),
            host="store-db",
            port=50057,
        )

        send(msg=ComponentMessage(input=x), host=self.host, port=self.port)

        return ComponentResponse(output=[0.0])


if __name__ == "__main__":
    host = os.environ.get("HOST", "localhost")
    target_port = int(os.environ.get("TARGET_PORT", 50052))

    service = OfflineFeeder(host, target_port)
    start_server(service, port=int(os.environ.get("PORT")))
