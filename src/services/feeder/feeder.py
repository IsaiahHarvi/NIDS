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

from src.grpc_.services_pb2 import ComponentMessage, ComponentResponse
from src.grpc_.services_pb2_grpc import ComponentServicer
from src.grpc_.utils import sendto_mongo, sendto_service, start_server

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
        df = flow_row.to_frame().T
        # Drop unnecessary columns
        drop_columns = [
            "Flow_ID",
            "Timestamp",
            "Bwd_Avg_Packets/Bulk",
            "Bwd_Avg_Bulk_Rate",
            "Bwd_PSH_Flags",
            "Bwd_URG_Flags",
            "Fwd_Avg_Bytes/Bulk",
            "Fwd_Avg_Packets/Bulk",
            "Fwd_Avg_Bulk_Rate",
            "Bwd_Avg_Bytes/Bulk",
            "Fwd_Header_Length.1",
        ]
        df = df.drop(drop_columns, axis=1, errors="ignore")

        # Convert IP addresses to numeric format
        def change_ip(x):
            return sum([256**j * int(i) for j, i in enumerate(x.split(".")[::-1])])

        if "Source_IP" in df.columns:
            df["Source_IP"] = df["Source_IP"].apply(change_ip)
        if "Destination_IP" in df.columns:
            df["Destination_IP"] = df["Destination_IP"].apply(change_ip)

        df = df.replace([np.inf, -np.inf], np.nan).dropna()
        pd.set_option("display.max_rows", None)
        pd.set_option("display.max_columns", None)
        ic(df)
        x = df.select_dtypes(include=[float, int])

        x = StandardScaler().fit_transform(x)
        x = np.array(x).flatten()

        assert x.shape[0] == 73, f"Expected 73 features, got {x.shape[0]}"

        return x.tolist()

    def rename_cols(self, flow_data: pd.DataFrame) -> pd.DataFrame:
        # Mapping to CICIDS2017 feature names
        return flow_data.rename(
            columns={
                # IP and port information
                "src_ip": "Source_IP",
                "dst_ip": "Destination_IP",
                "src_port": "Source_Port",
                "dst_port": "Destination_Port",
                "protocol": "Protocol",
                # Flow duration and packet-related information
                "bidirectional_duration_ms": "Flow_Duration",
                "src2dst_packets": "Total_Fwd_Packets",
                "dst2src_packets": "Total_Backward_Packets",
                "src2dst_bytes": "Total_Length_of_Fwd_Packets",
                "dst2src_bytes": "Total_Length_of_Bwd_Packets",
                # Packet inter-arrival time (IAT) information
                "src2dst_min_piat_ms": "Fwd_IAT_Min",
                "src2dst_mean_piat_ms": "Fwd_IAT_Mean",
                "src2dst_stddev_piat_ms": "Fwd_IAT_Std",
                "src2dst_max_piat_ms": "Fwd_IAT_Max",
                "dst2src_min_piat_ms": "Bwd_IAT_Min",
                "dst2src_mean_piat_ms": "Bwd_IAT_Mean",
                "dst2src_stddev_piat_ms": "Bwd_IAT_Std",
                "dst2src_max_piat_ms": "Bwd_IAT_Max",
                "bidirectional_min_piat_ms": "Flow_IAT_Min",
                "bidirectional_mean_piat_ms": "Flow_IAT_Mean",
                "bidirectional_stddev_piat_ms": "Flow_IAT_Std",
                "bidirectional_max_piat_ms": "Flow_IAT_Max",
                # Packet size information
                "src2dst_min_ps": "Fwd_Packet_Length_Min",
                "src2dst_mean_ps": "Fwd_Packet_Length_Mean",
                "src2dst_stddev_ps": "Fwd_Packet_Length_Std",
                "src2dst_max_ps": "Fwd_Packet_Length_Max",
                "dst2src_min_ps": "Bwd_Packet_Length_Min",
                "dst2src_mean_ps": "Bwd_Packet_Length_Mean",
                "dst2src_stddev_ps": "Bwd_Packet_Length_Std",
                "dst2src_max_ps": "Bwd_Packet_Length_Max",
                "bidirectional_min_ps": "Flow_Packet_Length_Min",
                "bidirectional_mean_ps": "Flow_Packet_Length_Mean",
                "bidirectional_stddev_ps": "Flow_Packet_Length_Std",
                "bidirectional_max_ps": "Flow_Packet_Length_Max",
                # TCP flag-related fields
                "src2dst_syn_packets": "Fwd_PSH_Flags",
                "bidirectional_syn_packets": "Fwd_Syn_Flags",
                "bidirectional_ack_packets": "Fwd_Ack_Flags",
                "bidirectional_psh_packets": "Fwd_PSH_Flags",
                "bidirectional_urg_packets": "Fwd_URG_Flags",
                "bidirectional_cwr_packets": "Fwd_CWR_Flags",
                "bidirectional_ece_packets": "Fwd_ECE_Flags",
                "bidirectional_rst_packets": "Fwd_RST_Flags",
                "bidirectional_fin_packets": "Fwd_FIN_Flags",
                # ACK and other TCP packet counters
                "src2dst_ack_packets": "Fwd_Ack_Flags",
                "src2dst_psh_packets": "Fwd_PSH_Flags",
                "src2dst_rst_packets": "Fwd_RST_Flags",
                "src2dst_fin_packets": "Fwd_FIN_Flags",
                "dst2src_syn_packets": "Bwd_Syn_Flags",
                "dst2src_ack_packets": "Bwd_Ack_Flags",
                "dst2src_rst_packets": "Bwd_RST_Flags",
                "dst2src_fin_packets": "Bwd_FIN_Flags",
            }
        )


if __name__ == "__main__":
    interface = os.environ.get("INTERFACE", "eth0")
    duration = int(os.environ.get("DURATION", 10))

    service = Feeder(interface, duration)
    start_server(service, port=int(os.environ.get("PORT")))
