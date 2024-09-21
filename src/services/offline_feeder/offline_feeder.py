import os
import numpy as np
import pandas as pd

from src.grpc_.services_pb2 import ComponentMessage, ComponentResponse
from src.grpc_.services_pb2_grpc import ComponentServicer 
from src.grpc_.utils import start_server, sendto_service, sendto_mongo

# from sklearn.preprocessing import StandardScaler
from uuid import uuid4 as UUID

from icecream import ic

ic.configureOutput(includeContext=False)


class OfflineFeeder(ComponentServicer):
    def __init__(self) -> None:
        ic(f"Started on {os.environ.get('PORT')}")

    def forward(self, msg: ComponentMessage, context) -> ComponentResponse:
        uuid = str(UUID())
        if msg.health_check:
            ic("Health check")
            return ComponentResponse(flow=msg.flow)

        df = pd.read_csv("data/CIC/test_data.csv")
        df.columns = (
            df.columns.str.strip()
            .str.replace(" ", "_")
            .str.replace("/", "_")
            .str.replace(".", "_")
        )
        full_sample = df.sample(n=1)
        metadata = {
            col: str(full_sample[col].values[0]) 
            for col in list(full_sample.columns)
        }

        y = full_sample["Label"].values[0]
        sample = full_sample.drop(
            ["Flow_ID", "Source_IP", "Destination_IP", "Timestamp", "Label"],
            axis=1,
            errors="ignore",
        )
        sample = sample.select_dtypes(include=[float, int])
        sample.replace([np.inf, -np.inf], np.nan, inplace=True)
        sample.fillna(sample.mean(), inplace=True)
        x = sample.iloc[0].to_numpy().flatten()
        # scaler = StandardScaler()
        # x = scaler.fit_transform(np.expand_dims(data, axis=0)).squeeze(0).tolist()
        # ic(scaler.mean_, scaler.scale_)
        ic(y)
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
