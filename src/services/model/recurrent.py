import torch
from ai.BasicModule import BasicModule
from icecream import ic
from src.grpc.services_pb2 import ComponentMessage, ComponentResponse
from src.grpc.services_pb2_grpc import ComponentServicer
from src.grpc.utils import start_server

class RecurrentModel(ComponentServicer):
    def __init__(self):
        self.model = BasicModule.load_from_checkpoint(
            "data/checkpoints/RNN.ckpt", 
            model_constructor_kwargs={"batch_size": 1}
        )

    def forward(self, request, context):
        x = torch.tensor(request.input) 
        match x.dim():
            case 1:
                x = x.view(1, 1, -1)
            case 2:
                x = x.unsqueeze(0) # add batch dimension

        assert x.dim() == 3, f"Expected [batch_size, seq_len, input_size] but got {x.shape}"

        pred = torch.argmax(self.model(x), dim=1).item()
        # ic(pred)
        return ComponentResponse(output=pred)

if __name__ == "__main__":
    service = RecurrentModel()
    start_server(service, port=50051)
