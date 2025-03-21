import os

import torch
from icecream import ic

from ai.BasicModule import BasicModule
from src.grpc_.services_pb2 import ComponentMessage, ComponentResponse
from src.grpc_.services_pb2_grpc import ComponentServicer
from src.grpc_.utils import start_server

ic.configureOutput(includeContext=False)


class NeuralNetwork(ComponentServicer):
    def __init__(self, ckpt_path: str) -> None:
        os.environ["CUDA_VISIBLE_DEVICES"] = ""
        self.model = BasicModule.load_from_checkpoint(
            checkpoint_path=ckpt_path, strict=False
        ).to("cpu")
        self.model.eval()
        ic(f"Started on {os.environ.get('PORT')}")

    def forward(self, msg: ComponentMessage, context) -> ComponentResponse:
        if msg.health_check:
            ic("Health check")
            return ComponentResponse(return_code=0)

        x = torch.tensor(msg.flow)
        # ic(x.shape)

        x = x.unsqueeze(0) if x.dim() == 1 else x
        assert x.dim() == 2, f"Expected shape [0, input_size] but got {x.shape}"

        pred = torch.argmax(self.model(x), dim=1).item()
        ic(pred)

        return ComponentResponse(prediction=pred, return_code=0)


if __name__ == "__main__":
    service = NeuralNetwork(ckpt_path="model.ckpt")
    start_server(service, port=int(os.environ.get("PORT")))
