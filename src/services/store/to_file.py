import os
import pandas as pd

from src.grpc_.services_pb2 import ComponentMessage, ComponentResponse
from src.grpc_.services_pb2_grpc import ComponentServicer
from src.grpc_.utils import start_server

from icecream import ic

ic.configureOutput(includeContext=False)


class StoreFile(ComponentServicer):
    def __init__(self, file_name: str) -> None:
        self.output_file = file_name
        ic(f"Started on {os.environ.get('PORT')}")

    def forward(self, msg: ComponentMessage, context) -> ComponentResponse:
        if msg.health_check:
            ic("Health check")
            return ComponentResponse(output=msg.input)

        # ic(msg.input)
        df = pd.DataFrame([msg.input])

        if not os.path.isfile(self.output_file):
            df.to_csv(self.output_file, index=False, header=True)
            ic(f"Created new file: {self.output_file}")
        else:
            df.to_csv(self.output_file, mode="a", index=False, header=False)
            ic(f"Appended to: {self.output_file}")

        return ComponentResponse(output=[0.0])


if __name__ == "__main__":
    service = StoreFile(file_name=os.environ.get("CSV_OUT_NAME", "output.csv"))
    start_server(service, port=int(os.environ.get("PORT")))
