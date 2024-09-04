import grpc
import os
import numpy as np
import pandas as pd

from src.grpc_.services_pb2 import ComponentMessage, ComponentResponse
from src.grpc_.services_pb2_grpc import ComponentServicer, ComponentStub
from src.grpc_.utils import start_server, send
from sklearn.preprocessing import StandardScaler
from uuid import uuid4 as UUID

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
        df.columns = df.columns.str.strip().str.replace(" ", "_")
        df = df.drop(
            ["Flow_ID", "Source_IP", "Destination_IP", "Timestamp"],
            axis=1,
            errors="ignore",
        )
        sample = df.sample(n=1)
        y = sample["Label"].values[0]
        sample = sample.select_dtypes(include=[float, int])
        sample.replace([np.inf, -np.inf], np.nan, inplace=True)
        sample.fillna(sample.mean(), inplace=True)

        sample = sample.drop("Label", axis=1, errors='ignore').iloc[0].to_numpy()
        x = sample.flatten()
        
        # scaler = StandardScaler()
        # x = scaler.fit_transform(np.expand_dims(data, axis=0)).squeeze(0).tolist()
        # ic(scaler.mean_, scaler.scale_)

        ic(y)
        send(
            msg=ComponentMessage(
                input=x,
                collection_name=self.__class__.__name__,
                mongo_id=str(UUID() if not msg.mongo_id else msg.mongo_id),
                prediction=-1,
            ),
            host="store-db",
            port=50057,
        )

        send(msg=ComponentMessage(input=x), host=self.host, port=self.port)

        return ComponentResponse(output=x)


if __name__ == "__main__":
    host = os.environ.get("HOST", "localhost")
    target_port = int(os.environ.get("TARGET_PORT", 50052))

    service = OfflineFeeder(host, target_port)
    start_server(service, port=int(os.environ.get("PORT")))
