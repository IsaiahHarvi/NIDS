import torch
import os
from ai.BasicModule import BasicModule

from src.grpc_.services_pb2 import ComponentMessage, ComponentResponse
from src.grpc_.services_pb2_grpc import ComponentServicer
from src.grpc_.utils import start_server

from icecream import ic

ic.configureOutput(includeContext=False)


class NeuralNetwork(ComponentServicer):
    def __init__(self, ckpt_path: str) -> None:
        try:
            os.environ["CUDA_VISIBLE_DEVICES"] = ""
            self.model = BasicModule.load_from_checkpoint(
                checkpoint_path=ckpt_path, strict=False
            ).to("cpu")
        except Exception as e:
            raise RuntimeError(f"Failed to load the model from {ckpt_path}: {e}")
        self.model.eval()
        ic(f"Started on {os.environ.get('PORT')}")

    def forward(self, msg: ComponentMessage, context) -> ComponentResponse:
        if msg.health_check:
            ic("Health check")
            return ComponentResponse(flow=msg.flow)

        x = torch.tensor(msg.flow)
        # ic(x.shape)

        if x.dim() == 1:
            x = x.unsqueeze(0)
        assert x.dim() == 2, f"Expected shape [0, input_size] but got {x.shape}"

        pred = torch.argmax(self.model(x), dim=1).item()
        ic(pred)
        return ComponentResponse(prediction=pred, return_code=0)


if __name__ == "__main__":
    service = NeuralNetwork(ckpt_path="model.ckpt")
    start_server(service, port=int(os.environ.get("PORT")))
