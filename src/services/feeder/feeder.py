import pandas as pd
import subprocess
import os
import numpy as np

from src.grpc_.services_pb2 import ComponentMessage, ComponentResponse
from src.grpc_.services_pb2_grpc import ComponentServicer, ComponentStub
from src.grpc_.utils import start_server, send

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
        argus = self.pcap_to_argus(pcap)
        flow_csv = self.argus_to_flow_csv(
            argus, self.file_name.replace(".pcap", "_flows.csv")
        )
        flow_data = pd.read_csv(flow_csv)
        flow_row = flow_data.iloc[0].values
        flow_row = self.preprocess_flow_row(flow_row).tolist()

        send(
            msg=ComponentMessage(
                input=flow_row, collection_name=self.__class__.__name__
            ),
            host="store-db",
            port=50057,
        )

        send(
            msg=ComponentMessage(input=flow_row), host=self.host, port=self.port
        )

        return ComponentResponse(output=[0.0])

    def capture_pcap(self, interface: str, file_name: str, duration: int) -> str:
        pcap_file = file_name + (".pcap" if not file_name.endswith(".pcap") else "")
        cmd = ["tshark", "-i", interface, "-a", f"duration:{duration}", "-w", pcap_file]
        subprocess.run(cmd, check=True)
        ic(f"Captured packets to {pcap_file}")
        return pcap_file

    def pcap_to_argus(self, pcap_file: str) -> str:
        argus_file = pcap_file.replace(".pcap", ".argus")
        cmd = ["argus", "-r", pcap_file, "-w", argus_file]
        assert (
            subprocess.run(cmd, check=True).returncode == 0
        ), f"\n!!!Argus failed to process {pcap_file}!!!\n"
        ic(f"Converted {pcap_file} to Argus file {argus_file}")
        return argus_file

    def argus_to_flow_csv(self, argus_file: str, output_csv: str) -> str:
        cmd = [
            "ra",
            "-r",
            argus_file,
            "-c",
            ",",
            "-s",
            "stime,flgs,proto,saddr,daddr,sport,dport,bytes,pkts,state",
        ]
        assert subprocess.run(
            cmd, stdout=open(output_csv, "w"), check=True
        ), f"\n!!!Failed to convert {argus_file} to CSV!!!\n"
        ic(f"Converted Argus file {argus_file} to CSV: {output_csv}")
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
