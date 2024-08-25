import grpc
import pandas as pd
import subprocess
import os

from scapy.all import sniff, wrpcap
from src.grpc_.services_pb2 import ComponentMessage, ComponentResponse
from src.grpc_.services_pb2_grpc import ComponentServicer, ComponentStub
from src.grpc_.utils import start_server

from icecream import ic


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

        pcap_file = self.capture_pcap(self.interface, self.file_name, self.duration)
        csv_file = self.pcap_to_csv(pcap_file, self.file_name.replace(".pcap", ".csv"))
        flow_file = self.pcap_to_flow(csv_file, self.file_name.replace(".pcap", "_flows.csv"))
        # output = self.flow_to_model(flow_file, self.host, self.port)

        return ComponentResponse(output=[1., 0., 1.])

    def capture_pcap(self, interface: str, file_name: str, duration: int) -> str:
        packets = sniff(iface=interface, timeout=duration)
        file_name = file_name + (".pcap" if not file_name.endswith(".pcap") else "")
        wrpcap(file_name, packets)
        ic(f"Captured {len(packets)} packets to {file_name}")
        return file_name

    def pcap_to_csv(self, pcap_file: str, output_csv: str) -> str:
        cmd = [
            "tshark",
            "-r", pcap_file,
            "-T", "fields",
            "-e", "frame.number",
            "-e", "ip.src",
            "-e", "ip.dst",
            "-e", "frame.len",
            "-e", "frame.time",
            "-e", "ip.proto",
            "-E", "header=y",
            "-E", "separator=,", 
            "-E", "quote=d",
            "-E", "occurrence=f",
            "-E", "aggregator=,"
        ]

        with open(output_csv, "w") as output_file:
            subprocess.run(cmd, stdout=output_file)
        ic(f"Converted PCAP to CSV: {output_csv}")
        return output_csv

    def pcap_to_flow(self, input_pcap, output_csv) -> str:
        """
        Convert a CSV of packet data to a CSV of flow data
        """
        cmd = [
            "cicflowmeter",
            "-f", input_pcap,
            "-c", output_csv
        ]
        subprocess.run(cmd, check=True)
        ic(f"Converted {input_pcap} to flow {output_csv}")
        return output_csv

    def flow_to_model(self, flow_csv, model_host='localhost', model_port=50051) -> None:
        flow_data = pd.read_csv(flow_csv)
        flow_row = flow_data.iloc[0].values.tolist()

        with grpc.insecure_channel(f'{model_host}:{model_port}') as channel:
            stub = ComponentStub(channel)
            request = ComponentMessage(input=flow_row)
            response = stub.forward(request)
            print(f"Model Prediction: {response.output}")


if __name__ == "__main__":
    interface = os.environ.get("INTERFACE", "eth0")
    file_name = os.environ.get("FILE_NAME", "capture.pcap")
    duration = int(os.environ.get("DURATION", 10))
    host = os.environ.get("HOST", "localhost")
    target_port = int(os.environ.get("TARGET_PORT", 50052))

    service = Feeder(interface, file_name, duration, host, target_port)
    start_server(service, port=int(os.environ.get("PORT")))
