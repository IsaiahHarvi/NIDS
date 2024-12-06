import os
from uuid import uuid4 as UUID

import numpy as np
import pandas as pd
from icecream import ic
from sklearn.preprocessing import StandardScaler

from src.grpc_.services_pb2 import ComponentMessage, ComponentResponse
from src.grpc_.services_pb2_grpc import ComponentServicer
from src.grpc_.utils import sendto_mongo, sendto_service, start_server

ic.configureOutput(includeContext=False)


class OfflineFeeder(ComponentServicer):
    def __init__(self) -> None:
        ic(f"Started on {os.environ.get('PORT')}")

        df = pd.read_csv("data/CIC/test_data.csv", delimiter="\t")
        df["label"] = df["label"].str.lower().str.replace(r"[\s-]+", "_", regex=True)
        self.y = df["label"]

        self.metadata = df.copy()
        df.drop(
            [col for col in df.columns if "piat" not in col.lower()],
            axis=1,
            errors="ignore",
            inplace=True,
        )
        df = df.replace([np.inf, -np.inf], np.nan).dropna()
        x = df.select_dtypes(include=[float, int]).to_numpy()

        if x.shape[0] == 0:
            raise ValueError("Filtered dataset has zero rows.")

        self.x = StandardScaler().fit_transform(x)

    def forward(self, msg: ComponentMessage, context) -> ComponentResponse:
        uuid = str(UUID())
        if msg.health_check:
            ic("Health check")
            return ComponentResponse(return_code=0)

        idx = np.random.randint(0, len(self.x))
        x = self.x[idx]
        y = self.y[idx]
        metadata = self.metadata.iloc[idx].to_dict()
        ic(y, metadata, x.shape)

        model_response = sendto_service(
            msg=ComponentMessage(flow=x), host="neural-network", port=50052
        )
        pred: int = model_response.prediction

        sendto_mongo(
            {
                "id_": uuid,
                "flow_data": x.tolist(),
                "prediction": pred,
                "metadata": metadata,
            },
            collection_name=self.__class__.__name__,
        )
        return ComponentResponse(flow=x, return_code=0)


if __name__ == "__main__":
    service = OfflineFeeder()
    start_server(service, port=int(os.environ.get("PORT")))
