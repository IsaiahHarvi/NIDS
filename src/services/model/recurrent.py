import torch
import os
from ai.BasicModule import BasicModule

from src.grpc_.services_pb2 import ComponentMessage, ComponentResponse
from src.grpc_.services_pb2_grpc import ComponentServicer
from src.grpc_.utils import start_server

from icecream import ic

ic.configureOutput(includeContext=False)


class RecurrentModel(ComponentServicer):
    def __init__(self):
        self.model = BasicModule.load_from_checkpoint(
            "data/checkpoints/RNN.ckpt", model_constructor_kwargs={"batch_size": 1}
        )
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
        return ComponentResponse(prediction=pred)


if __name__ == "__main__":
    service = RecurrentModel()
    start_server(service, port=int(os.environ.get("PORT")))
