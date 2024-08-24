import torch
from ai.BasicModule import BasicModule
from icecream import ic
from src.grpc_.services_pb2 import ComponentMessage, ComponentResponse
from src.grpc_.services_pb2_grpc import ComponentServicer
from src.grpc_.utils import start_server

class ResidualModel(ComponentServicer):
    def __init__(self):
        self.model = BasicModule.load_from_checkpoint(
            "data/checkpoints/ResidualNetwork.ckpt", 
        )
        self.model.eval()
        ic("Started")

    def forward(self, msg: ComponentMessage, context):
        if msg.health_check:
            ic("Health check")
            return ComponentResponse(output=msg.input)

        x = torch.tensor(msg.input) 
        match x.dim():
            case 1:
                x = x.unsqueeze(0) # add batch dimension
            case 3:
                x = x.squeeze(1) # remove seq_len dimension

        assert x.dim() == 2, f"Expected [batch_size, input_size] but got {x.shape}"

        pred = torch.argmax(self.model(x), dim=1).item()
        # ic(pred)
        return ComponentResponse(prediction=pred)

if __name__ == "__main__":
    service = ResidualModel()
    start_server(service, port=50052)