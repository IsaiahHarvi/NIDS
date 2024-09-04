import torch
import os
from ai.BasicModule import BasicModule

from src.grpc_.services_pb2 import ComponentMessage, ComponentResponse
from src.grpc_.services_pb2_grpc import ComponentServicer
from src.grpc_.utils import start_server, send
from uuid import UUID

from icecream import ic

ic.configureOutput(includeContext=False)


class NeuralNetwork(ComponentServicer):
    def __init__(self, ckpt_path: str) -> None:
        self.model = BasicModule.load_from_checkpoint(ckpt_path)
        self.model.eval()
        ic(f"Started on {os.environ.get('PORT')}")

    def forward(self, msg: ComponentMessage, context):
        if msg.health_check:
            ic("Health check")
            return ComponentResponse(output=msg.input)

        x = torch.tensor(msg.input)
        match x.dim():
            case 1:
                x = x.view(1, 1, -1)
            case 2:
                x = x.unsqueeze(0)  # add batch dimension

        assert (
            x.dim() == 3
        ), f"Expected [batch_size, seq_len, input_size] but got {x.shape}"

        pred = torch.argmax(self.model(x), dim=1).item()
        # ic(pred)
        send(
            msg=ComponentMessage(
                prediction=pred,
                collection_name=self.__class__.__name__,
                mongo_id=(str(UUID()) if not msg.mongo_id else msg.mongo_id),
            ),
            host="store-db",
            port=50057,
        )
        return ComponentResponse(prediction=pred)


if __name__ == "__main__":
    ckpt_path = os.environ.get("MODEL_PATH", "data/checkpoints/ResidualNetwork.ckpt")
    service = NeuralNetwork(ckpt_path)
    start_server(service, port=int(os.environ.get("PORT")))
