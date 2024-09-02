import pandas as pd
import subprocess
import os
import numpy as np
from src.grpc_.services_pb2 import ComponentMessage, ComponentResponse
from src.grpc_.services_pb2_grpc import ComponentServicer, ComponentStub
from src.grpc_.utils import start_server, send
from sklearn.preprocessing import MinMaxScaler
from icecream import ic

ic.configureOutput(includeContext=False)

class Feeder(ComponentServicer):
    def __init__(self, interface, file_name, duration, host, port):
        self.interface = interface
        self.file_name = file_name
        self.duration = duration
        self.host = host
        self.port = port
        ic(f"Started on {os.environ.get('PORT')}")

    def forward(self, msg: ComponentMessage, context):
        if msg.health_check:
            ic("Health check")
            return ComponentResponse(output=msg.input)

        pcap = self.capture_pcap(self.interface, self.file_name, self.duration)
        flow_csv = self.pcap_to_flows(pcap)
        flow_data = pd.read_csv(flow_csv)
        flow_data.to_csv("/app/flow_data_output.csv", index=False)
        flow_row = flow_data.iloc[0].values
        flow_row = self.preprocess_flow_row(flow_row)
        flow_row = flow_row.reshape(1, -1)  # Reshape to (1, 80)
        x = MinMaxScaler().fit_transform(flow_row)
        x = x.squeeze(0).tolist()

        send(
            msg=ComponentMessage(input=x, collection_name=self.__class__.__name__),
            host="store-db",
            port=50057,
        )

        send(msg=ComponentMessage(input=x), host=self.host, port=self.port)

        return ComponentResponse(output=x)

    def capture_pcap(self, interface: str, file_name: str, duration: int) -> str:
        pcap_file = file_name + (".pcap" if not file_name.endswith(".pcap") else "")
        cmd = ["tshark", "-i", interface, "-a", f"duration:{duration}", "-w", pcap_file]
        subprocess.run(cmd, check=True)
        ic(f"Captured packets to {pcap_file}")
        return pcap_file

    def pcap_to_flows(self, pcap_file: str) -> str:
        output_csv = pcap_file.replace(".pcap", "_flows.csv")
        cicflowmeter_path = "/app/CICFlowMeter/CICFlowMeter-4.0/bin/CICFlowMeter"
        cmd = [cicflowmeter_path, "-f", pcap_file, "-c", output_csv]

        try:
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            ic(f"CICFlowMeter Output: {result.stdout}")
            ic(f"Converted PCAP file {pcap_file} to flow features in {output_csv}")
        except subprocess.CalledProcessError as e:
            ic(f"Error in CICFlowMeter: {e.stderr}")
            return None
        
        return output_csv

    def preprocess_flow_row(self, flow_row):
        numeric_row = []
        for value in flow_row:
            if isinstance(value, str) and value.strip() == "":
                numeric_row.append(0)  # Replace empty strings with zeros
            elif isinstance(value, str):
                try:
                    numeric_value = float(value)
                    numeric_row.append(numeric_value)
                except ValueError:
                    numeric_row.append(0)
            else:
                numeric_row.append(value)

        numeric_row = np.array(numeric_row)
        if numeric_row.shape[0] < 80:
            numeric_row = np.pad(
                numeric_row, (0, 80 - numeric_row.shape[0]), "constant"
            )
        elif numeric_row.shape[0] > 80:
            ic("WARNING: truncating row")
            numeric_row = numeric_row[:80]
        ic(f"reshaped to: {numeric_row.shape}")  # (80,)

        return numeric_row

if __name__ == "__main__":
    interface = os.environ.get("INTERFACE", "eth0")
    file_name = os.environ.get("FILE_NAME", "capture.pcap")
    duration = int(os.environ.get("DURATION", 10))
    host = os.environ.get("HOST", "neural-network")
    target_port = int(os.environ.get("TARGET_PORT", 50052))

    service = Feeder(interface, file_name, duration, host, target_port)
    start_server(service, port=int(os.environ.get("PORT")))
