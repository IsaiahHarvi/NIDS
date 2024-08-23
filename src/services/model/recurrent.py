import torch
from ai.BasicModule import BasicModule
from icecream import ic
from src.grpc.services_pb2 import ComponentMessage, ComponentResponse
from src.grpc.services_pb2_grpc import ComponentServicer
from src.grpc.utils import start_server

class RecurrentModel(ComponentServicer):
    def __init__(self):
        self.model = BasicModule.load_from_checkpoint("data/checkpoints/RNN.ckpt")

    def forward(self, request, context):
        x = torch.tensor(request.input)
        if x.dim() == 1:
            x = x.unsqueeze(0)
        ic(x.dim())         
        pred = torch.argmax(self.model(x), dim=1)
        # ic(pred) 
        return ComponentResponse(output=pred.item())

if __name__ == "__main__":
    service = RecurrentModel()
    start_server(service, port=50051)
