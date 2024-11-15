import os
import tempfile
import time
from typing import Dict, List, Tuple
from uuid import uuid4 as UUID

import dpkt
import numpy as np
import pandas as pd
import pcap
from icecream import ic
from nfstream import NFStreamer
from sklearn.preprocessing import StandardScaler

from pcaps.utils import rename_cols
from src.grpc_.services_pb2 import ComponentMessage, ComponentResponse
from src.grpc_.services_pb2_grpc import ComponentServicer
from src.grpc_.utils import sendto_mongo, sendto_service, start_server

ic.configureOutput(includeContext=False)


class Feeder(ComponentServicer):
    def __init__(self, interface, duration):
        self.interface = interface
        self.duration = duration
        ic(f"Started on {os.environ.get('PORT')}")

    def forward(self, msg: ComponentMessage, context) -> ComponentResponse:
        uuid = str(UUID())
        if msg.health_check:
            ic("Health check")
            return ComponentResponse(return_code=0)

        flows, metadata_list = self.get_flows(self.interface, self.duration)

        for i, flow_row in enumerate(flows):
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

        # temporary PCAP file
        with tempfile.NamedTemporaryFile(suffix=".pcap", delete=True) as temp_pcap:
            writer = dpkt.pcap.Writer(temp_pcap)
            for pkt in captured_packets:
                writer.writepkt(pkt)

            flow_data = NFStreamer(
                source=temp_pcap.name, statistical_analysis=True
            ).to_pandas()
        flow_data = rename_cols(flow_data)

        # Convert flow data into a list of flows and metadata
        flow_list = flow_data.to_dict(orient="records")
        metadata_list = [
            {col: str(flow_data[col].iloc[i]) for col in flow_data.columns}
            for i in range(len(flow_data))
        ]

        ic(f"Captured {len(flow_list)} flows and metadata")
        return flow_list, metadata_list

    def preprocessor(self, flow_row: pd.Series) -> list:
        df = flow_row.to_frame().T
        # Drop unnecessary columns
        drop_columns = [
            "id",
            "expiration_id",
            "src_ip",
            "src_mac",
            "src_oui",
            "src_port",
            "dst_ip",
            "dst_mac",
            "dst_oui",
            "dst_port",
            "flow_id",
            "flow_start",
            "bidirectional_first_seen_ms",
            "bidirectional_last_seen_ms",
            "src2dst_first_seen_ms",
            "src2dst_last_seen_ms",
            "dst2src_first_seen_ms",
            "dst2src_last_seen_ms" "label",
        ]

        df = df.drop(drop_columns, axis=1, errors="ignore")
        df = df.replace([np.inf, -np.inf], np.nan).dropna()

        x = df.select_dtypes(include=[float, int])
        x = StandardScaler().fit_transform(x)
        x = np.array(x).flatten()

        assert x.shape[0] == 71, f"Expected 71 features, got {x.shape[0]}"

        return x.tolist()


if __name__ == "__main__":
    interface = os.environ.get("INTERFACE", "eth0")
    duration = int(os.environ.get("DURATION", 10))

    service = Feeder(interface, duration)
    start_server(service, port=int(os.environ.get("PORT")))
