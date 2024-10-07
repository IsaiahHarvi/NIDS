import os
import random
from uuid import uuid4 as UUID

from icecream import ic

from src.ai.DataModule import DataModule
from src.grpc_.services_pb2 import ComponentMessage, ComponentResponse
from src.grpc_.services_pb2_grpc import ComponentServicer
from src.grpc_.utils import sendto_mongo, sendto_service, start_server

ic.configureOutput(includeContext=False)


class OfflineFeeder(ComponentServicer):
    def __init__(self) -> None:
        ic(f"Started on {os.environ.get('PORT')}")

    def forward(self, msg: ComponentMessage, context) -> ComponentResponse:
        uuid = str(UUID())
        if msg.health_check:
            ic("Health check")
            return ComponentResponse(return_code=0)

        dm = DataModule(
            paths=["data/CIC/test_data.csv"],
            val_split=0.9,
            batch_size=1,
            num_workers=1,
        )
        dm.setup()

        idx = random.randint(0, len(dm.val_dataset) - 1)
        x, y = dm.val_dataset[idx]
        metadata = dm.get_metadata(idx)

        ic(x.shape)
        ic(y.item())
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
