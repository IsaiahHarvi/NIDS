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
    def __init__(self) -> None:
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

        sample_row = sample.drop("Label", axis=1, errors="ignore").iloc[0]
        x = sample_row.to_numpy().flatten()

        # scaler = StandardScaler()
        # x = scaler.fit_transform(np.expand_dims(data, axis=0)).squeeze(0).tolist()
        # ic(scaler.mean_, scaler.scale_)

        ic(y)
        uuid = str(UUID() if not msg.mongo_id else msg.mongo_id)
        send(  # send the metadata
            msg={
                "id_": uuid,
                "collection_name": self.__class__.__name__,
                "input": x,
                "metadata": {col: str(sample_row[col]) for col in sample_row.index},
            },
            host="store-db",
            port=50057,
        )

        send(msg=ComponentMessage(input=x), host="neural-network", port=50052)

        return ComponentResponse(output=x)


if __name__ == "__main__":
    service = OfflineFeeder()
    start_server(service, port=int(os.environ.get("PORT")))
