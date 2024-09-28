import pandas as pd
import os
import numpy as np
import dpkt
import pcap
import time

from typing import List, Dict, Tuple
from src.grpc_.services_pb2 import ComponentMessage, ComponentResponse
from src.grpc_.services_pb2_grpc import ComponentServicer
from src.grpc_.utils import start_server, sendto_service, sendto_mongo
from nfstream import NFStreamer

from uuid import uuid4 as UUID
from icecream import ic

ic.configureOutput(includeContext=False)


class Feeder(ComponentServicer):
    def __init__(self, interface, duration):
        self.interface = interface
        self.duration = duration
        ic(f"Started on {os.environ.get('PORT')}")

    def forward(self, msg: ComponentMessage, context):
        uuid = str(UUID())
        if msg.health_check:
            ic("Health check")
            return ComponentResponse(return_code=0)

        flows, metadata_list = self.get_flows(self.interface, self.duration)

        for i, flow_row in enumerate(flows):
            # Preprocess each flow row to match training features
            x = self.preprocessor(pd.Series(flow_row))

            model_response = sendto_service(
                msg=ComponentMessage(flow=x),
                host="127.0.0.1",  # "neural-network",
                port=50052,
            )
            pred: int = model_response.prediction

            sendto_mongo(
                {
                    "id_": uuid,
                    "flow_data": x,
                    "prediction": pred,
                    "metadata": metadata_list[i],
                },
                collection_name=self.__class__.__name__,
            )

        return ComponentResponse(return_code=0)

    def get_flows(self, interface: str, duration: int) -> Tuple[List[Dict], List[Dict]]:
        ic(f"Capturing packets from {interface} for {duration} seconds")

        captured_packets = []
        pc = pcap.pcap(name=interface, promisc=True, immediate=True, timeout_ms=50)
        start_time = time.time()

        for _, pkt in pc:
            if (time.time() - start_time) > duration:
                break
            # decode using dpkt
            eth = dpkt.ethernet.Ethernet(pkt)
            ip = eth.data
            if isinstance(ip, dpkt.ip.IP):
                captured_packets.append(pkt)

        # Convert to flows
        stream = NFStreamer(
            source=captured_packets, statistical_analysis=True, bidirectional=True
        )
        flow_data = stream.to_pandas()
        flow_data = self.rename_cols(flow_data)

        # Convert flow data into a list of flows and metadata
        flow_list = flow_data.to_dict(orient="records")
        metadata_list = [
            {col: str(flow_data[col].iloc[i]) for col in flow_data.columns}
            for i in range(len(flow_data))
        ]

        ic(f"Captured {len(flow_list)} flows and metadata")
        return flow_list, metadata_list

    def preprocessor(self, flow_row: pd.Series) -> list:
        flow_row_df = flow_row.to_frame().T
        numeric_row = flow_row_df.select_dtypes(include=[float, int]).fillna(0)
        numeric_row.replace([np.inf, -np.inf], np.nan, inplace=True)
        numeric_row.fillna(numeric_row.mean(), inplace=True)
        numeric_row = np.array(numeric_row).flatten()

        assert numeric_row.shape[0] == 72, f"Expected 72 features, got {numeric_row.shape[0]}"

        return numeric_row.tolist()

    def rename_cols(flow_data: pd.DataFrame) -> pd.DataFrame:
        # Select the relevant features used in training, renamed to match CICIDS2017 feature names
        return flow_data.rename(
            columns={
                "src_ip": "Source IP",
                "dst_ip": "Destination IP",
                "src_port": "Source Port",
                "dst_port": "Destination Port",
                "protocol": "Protocol",
                "bidirectional_duration_ms": "Flow Duration",
                "src2dst_packets": "Total Fwd Packets",
                "dst2src_packets": "Total Backward Packets",
                "src2dst_bytes": "Total Length of Fwd Packets",
                "dst2src_bytes": "Total Length of Bwd Packets",
                "src2dst_duration_ms": "Fwd Packet Length Mean",
                "dst2src_duration_ms": "Bwd Packet Length Mean",
                "src2dst_mean_piat_ms": "Fwd IAT Mean",
                "dst2src_mean_piat_ms": "Bwd IAT Mean",
                "bidirectional_mean_piat_ms": "Flow IAT Mean",
                "src2dst_stddev_piat_ms": "Fwd IAT Std",
                "dst2src_stddev_piat_ms": "Bwd IAT Std",
                "bidirectional_stddev_piat_ms": "Flow IAT Std",
                "src2dst_min_piat_ms": "Fwd IAT Min",
                "dst2src_min_piat_ms": "Bwd IAT Min",
                "src2dst_max_piat_ms": "Fwd IAT Max",
                "dst2src_max_piat_ms": "Bwd IAT Max",
                "bidirectional_min_piat_ms": "Flow IAT Min",
                "bidirectional_max_piat_ms": "Flow IAT Max",
                "src2dst_syn_packets": "Fwd PSH Flags",
                "src2dst_ack_packets": "Fwd URG Flags",
                "dst2src_syn_packets": "Bwd PSH Flags",
                "dst2src_ack_packets": "Bwd URG Flags",
            }
        )


if __name__ == "__main__":
    interface = os.environ.get("INTERFACE", "eth0")
    duration = int(os.environ.get("DURATION", 10))

    service = Feeder(interface, duration)
    start_server(service, port=int(os.environ.get("PORT")))
