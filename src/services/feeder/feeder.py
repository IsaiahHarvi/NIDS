import pandas as pd
import os
import numpy as np
import dpkt
import pcap
import time

from typing import Tuple
from src.grpc_.services_pb2 import ComponentMessage, ComponentResponse
from src.grpc_.services_pb2_grpc import ComponentServicer
from src.grpc_.utils import start_server, sendto_service, sendto_mongo
from nfstream import NFStreamer

# from sklearn.preprocessing import StandardScaler
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
        uuid = str(UUID())
        if msg.health_check:
            ic("Health check")
            return ComponentResponse(flow=msg.flow)

        pcap = self.capture_pcap(self.interface, self.file_name, self.duration)
        flow_csv, metadata = self.pcap_to_flows(pcap)
        flow_data = pd.read_csv(flow_csv)
        flow_row = self.preprocess_flow_row(flow_data.iloc[0])
        x = flow_row.tolist()

        # scaler = StandardScaler()
        # x = scaler.fit_transform(np.expand_dims(data, axis=0)).squeeze(0).tolist()
        # ic(scaler.mean_, scaler.scale_)

        model_response = sendto_service(
            msg=ComponentMessage(flow=x),
            host="127.0.0.1",  #  "neural-network",
            port=50052,
        )
        pred: int = model_response.prediction

        sendto_mongo(
            {"id_": uuid, "flow_data": x, "prediction": pred, "metadata": metadata},
            collection_name=self.__class__.__name__,
        )

        return ComponentResponse(flow=x)

    def capture_pcap(self, interface: str, file_name: str, duration: int) -> str:
        ic(f"Capturing packets from {interface} for {duration} seconds")
        pcap_file = file_name + (".pcap" if not file_name.endswith(".pcap") else "")
        pc = pcap.pcap(name=interface, promisc=True, immediate=True, timeout_ms=50)

        with open(pcap_file, 'wb') as f:
            writer = dpkt.pcap.Writer(f)
            start_time = time.time()
            for ts, pkt in pc:
                if (time.time() - start_time) > duration:

                    break
                writer.writepkt(pkt, ts)

        ic(f"Captured packets to {pcap_file}")
        return pcap_file

    def pcap_to_flows(self, pcap_file: str) -> Tuple[str, dict]:
        output_csv = pcap_file.replace(".pcap", "_flows.csv")
        stream = NFStreamer(source=pcap_file)
        flow_data = stream.to_pandas()
        # ic(flow_data.columns)

        features = pd.DataFrame()
        features["Source_IP"] = flow_data["src_ip"]
        features["Destination_IP"] = flow_data["dst_ip"]
        features["Source_Port"] = flow_data["src_port"]
        features["Destination_Port"] = flow_data["dst_port"]
        features["Protocol"] = flow_data["protocol"]
        features["Flow_Duration"] = flow_data["bidirectional_duration_ms"]
        features["Total_Fwd_Packets"] = flow_data["src2dst_packets"]
        features["Total_Backward_Packets"] = flow_data["dst2src_packets"]
        features["Total_Length_of_Fwd_Packets"] = flow_data["src2dst_bytes"]
        features["Total_Length_of_Bwd_Packets"] = flow_data["dst2src_bytes"]

        # Calculate flows per second and bytes per second
        features["Flow_Bytes_s"] = (
            features["Total_Length_of_Fwd_Packets"]
            + features["Total_Length_of_Bwd_Packets"]
        ) / (features["Flow_Duration"] / 1000)
        features["Flow_Packets_s"] = (
            features["Total_Fwd_Packets"] + features["Total_Backward_Packets"]
        ) / (features["Flow_Duration"] / 1000)

        # Forward Packet Length Mean and Standard Deviation (calculated from total bytes and packet count)
        features["Fwd_Packet_Length_Mean"] = (
            features["Total_Length_of_Fwd_Packets"] / features["Total_Fwd_Packets"]
        )
        features["Bwd_Packet_Length_Mean"] = (
            features["Total_Length_of_Bwd_Packets"] / features["Total_Backward_Packets"]
        )

        features["Timestamp"] = pd.to_datetime(
            flow_data["bidirectional_first_seen_ms"], unit="ms"
        )

        # features["Fwd_Packet_Length_Max"] =
        # features["Fwd_Packet_Length_Min"] =
        # features["Fwd_Packet_Length_Mean"] =

        # features["Bwd_Packet_Length_Max"] =
        # features["Bwd_Packet_Length_Min"] =
        # features["Bwd_Packet_Length_Mean"] =

        # features.to_csv("/app/flow_data_output.csv", index=False)  # for surgery
        metadata = {col: str(features[col].iloc[0]) for col in features.columns}

        rel_features = features.drop(
            ["Source_IP", "Destination_IP", "Timestamp"], axis=1, errors="ignore"
        )
        rel_features.to_csv(output_csv, index=False)

        ic(f"Converted PCAP file {pcap_file} to flow features in {output_csv}")
        return output_csv, metadata

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
        ic(f"reshaped to: {numeric_row.shape}")  # (80,)

        return numeric_row


if __name__ == "__main__":
    interface = os.environ.get("INTERFACE", "eth0")
    file_name = os.environ.get("FILE_NAME", "capture.pcap")
    duration = int(os.environ.get("DURATION", 10))

    service = Feeder(interface, file_name, duration)
    start_server(service, port=int(os.environ.get("PORT")))
