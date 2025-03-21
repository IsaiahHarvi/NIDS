import os
import tempfile
import time
from typing import Dict, List, Tuple
from uuid import uuid4 as UUID

import dpkt
import numpy as np
import pandas as pd
import pcap
import torch
from icecream import ic
from nfstream import NFStreamer
from sklearn.preprocessing import StandardScaler

from ai.BasicModule import BasicModule
from src.grpc_.services_pb2 import ComponentMessage, ComponentResponse
from src.grpc_.services_pb2_grpc import ComponentServicer
from src.grpc_.utils import sendto_mongo, start_server


class Feeder(ComponentServicer):
    def __init__(self, interface, duration):
        self.interface = interface
        self.duration = duration

        os.environ["CUDA_VISIBLE_DEVICES"] = ""
        self.model = BasicModule.load_from_checkpoint(
            checkpoint_path="model.ckpt", strict=False
        ).to("cpu")
        self.model.eval()

        ic(f"Started on {os.environ.get('PORT')} | PID: {os.getpid()}")

    def forward(self, msg: ComponentMessage, context) -> ComponentResponse:
        uuid = str(UUID())
        if msg.health_check:
            ic("Health check")
            return ComponentResponse(return_code=0)

        flows, metadata_list = self.get_flows(self.interface, self.duration)

        records: List[dict] = []
        for i, flow_row in enumerate(flows):
            x = self.preprocessor(pd.Series(flow_row))

            # model_response = sendto_service(
            #     msg=ComponentMessage(flow=x),
            #     host="127.0.0.1",  # "neural-network",
            #     port=50052,
            # )

            x = torch.tensor(x, dtype=torch.float32)
            x = x.unsqueeze(0) if x.dim() == 1 else x
            pred = torch.argmax(self.model(x), dim=1).item()

            records.append(
                {
                    "id_": uuid,
                    "flow_data": x.tolist(),
                    "prediction": pred,
                    "metadata": metadata_list[i],
                }
            )

        if records:
            sendto_mongo(
                data=records,
                collection_name=self.__class__.__name__,
            )

        return ComponentResponse(return_code=bool(records))

    def get_flows(self, interface: str, duration: int) -> Tuple[List[Dict], List[Dict]]:
        ic(f"Capturing packets from {interface} for {duration} seconds")

        captured_packets = []
        start_time = time.time()

        try:
            for _, pkt in pcap.pcap(
                name=interface, promisc=True, immediate=True, timeout_ms=50
            ):
                if (time.time() - start_time) > duration:
                    break
                eth = dpkt.ethernet.Ethernet(pkt)
                if isinstance(eth.data, dpkt.ip.IP):
                    captured_packets.append(pkt)
        except Exception as e:
            ic(e)

        if not captured_packets:
            ic("No packets captured")
            return [], []

        # temporary PCAP file
        with tempfile.NamedTemporaryFile(suffix=".pcap", delete=True) as temp_pcap:
            writer = dpkt.pcap.Writer(temp_pcap)
            for pkt in captured_packets:
                writer.writepkt(pkt)

            flow_data = NFStreamer(
                source=temp_pcap.name, statistical_analysis=True
            ).to_pandas()

        flow_list = flow_data.to_dict(orient="records")
        metadata_list = [
            {col: str(flow_data[col].iloc[i]) for col in flow_data.columns}
            for i in range(len(flow_data))
        ]

        ic(f"Captured {len(flow_list)} flows and metadata")
        return flow_list, metadata_list

    def preprocessor(self, flow_row: pd.Series) -> list:
        df = flow_row.to_frame().T
        df.drop(
            [col for col in df.columns if "piat" not in col.lower()],
            axis=1,
            errors="ignore",
            inplace=True,
        )

        df = df.replace([np.inf, -np.inf], np.nan).infer_objects(copy=False).dropna()
        x = df.select_dtypes(include=[float, int]).to_numpy()

        x = StandardScaler().fit_transform(x)
        return np.array(x).flatten()


if __name__ == "__main__":
    ic.configureOutput(includeContext=False)

    interface = os.environ.get("INTERFACE", "eth0")
    duration = int(os.environ.get("DURATION", 5))

    service = Feeder(interface, duration)
    start_server(service, port=int(os.environ.get("PORT")))
