import pandas as pd
import subprocess
import os
import numpy as np
from src.grpc_.services_pb2 import ComponentMessage, ComponentResponse
from src.grpc_.services_pb2_grpc import ComponentServicer, ComponentStub
from src.grpc_.utils import start_server, send
from nfstream import NFStreamer
from sklearn.preprocessing import StandardScaler
from uuid import uuid4 as UUID


from icecream import ic

ic.configureOutput(includeContext=False)


class Feeder(ComponentServicer):
    def __init__(self, interface, file_name, duration):
        self.interface = interface
        self.file_name = file_name
        self.duration = duration
        ic(f"Started on {os.environ.get('PORT')}")

    def forward(self, msg: ComponentMessage, context):
        if msg.health_check:
            ic("Health check")
            return ComponentResponse(output=msg.input)

        pcap = self.capture_pcap(self.interface, self.file_name, self.duration)
        flow_csv = self.pcap_to_flows(pcap)
        flow_data = pd.read_csv(flow_csv)
        flow_row = self.preprocess_flow_row(flow_data.iloc[0])

        x = StandardScaler().fit_transform(flow_row.reshape(1, -1)).squeeze(0).tolist()

        uuid = str(UUID())
        send(
            msg=ComponentMessage(
                input=x,
                collection_name=self.__class__.__name__,
                mongo_id=uuid,  # feeder is never recipient
                prediction=-1,
            ),
            host="store-db",
            port=50057,
        )
        send(
            msg=ComponentMessage(input=x, mongo_id=uuid),
            host="neural-network",
            port=50052,
        )

        return ComponentResponse(output=x)

    def capture_pcap(self, interface: str, file_name: str, duration: int) -> str:
        pcap_file = file_name + (".pcap" if not file_name.endswith(".pcap") else "")
        cmd = ["tshark", "-i", interface, "-a", f"duration:{duration}", "-w", pcap_file]
        subprocess.run(cmd, check=True)
        ic(f"Captured packets to {pcap_file}")
        return pcap_file

    def pcap_to_flows(self, pcap_file: str) -> str:
        output_csv = pcap_file.replace(".pcap", "_flows.csv")
        stream = NFStreamer(source=pcap_file)
        flow_data = stream.to_pandas()

        features = pd.DataFrame()
        features["Source_Port"] = flow_data["src_port"]
        features["Destination_Port"] = flow_data["dst_port"]
        features["Protocol"] = flow_data["protocol"]
        features["Flow_Duration"] = flow_data["bidirectional_duration_ms"]
        features["Total_Fwd_Packets"] = flow_data["src2dst_packets"]
        features["Total_Backward_Packets"] = flow_data["dst2src_packets"]
        features["Total_Length_of_Fwd_Packets"] = flow_data["src2dst_bytes"]
        features["Total_Length_of_Bwd_Packets"] = flow_data["dst2src_bytes"]
        features["Flow_Bytes/s"] = (
            features["Total_Length_of_Fwd_Packets"]
            + features["Total_Length_of_Bwd_Packets"]
        ) / (features["Flow_Duration"] / 1000)
        features["Flow_Packets/s"] = (
            features["Total_Fwd_Packets"] + features["Total_Backward_Packets"]
        ) / (features["Flow_Duration"] / 1000)

        features.to_csv("/app/flow_data_output.csv", index=False)  # for surgery
        features.to_csv(output_csv, index=False)

        ic(f"Converted PCAP file {pcap_file} to flow features in {output_csv}")
        return output_csv

    def preprocess_flow_row(self, flow_row: pd.Series):
        flow_row_df = flow_row.to_frame().T
        numeric_row = flow_row_df.select_dtypes(include=[float, int]).fillna(0)
        numeric_row.replace([np.inf, -np.inf], np.nan, inplace=True)
        numeric_row.fillna(numeric_row.mean(), inplace=True)
        numeric_row = np.array(numeric_row).flatten()

        if numeric_row.shape[0] < 80:
            numeric_row = np.pad(
                numeric_row, (0, 80 - numeric_row.shape[0]), "constant"
            )
            ic("WARNING: padding row")
        elif numeric_row.shape[0] > 80:
            numeric_row = numeric_row[:80]
            ic("WARNING: truncating row")

        ic(f"reshaped to: {numeric_row.shape}")  # (80,)

        return numeric_row


if __name__ == "__main__":
    interface = os.environ.get("INTERFACE", "eth0")
    file_name = os.environ.get("FILE_NAME", "capture.pcap")
    duration = int(os.environ.get("DURATION", 10))

    service = Feeder(interface, file_name, duration)
    start_server(service, port=int(os.environ.get("PORT")))
