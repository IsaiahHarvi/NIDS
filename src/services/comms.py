"""
Simple method to interact with the gRPC services oustide of the test suite.
"""
import click
import grpc
from src.grpc_.services_pb2 import ComponentMessage
from src.grpc_.services_pb2_grpc import ComponentStub

from icecream import ic


@click.command()
@click.option('--port', default=50054, help='Port of the service to connect to.')
def main(port):
    match port:
        case 50051 | 50052:
            # Connect to Recurrent or Residual service
            with grpc.insecure_channel(f"localhost:{port}") as channel:
                stub = ComponentStub(channel)
                request = ComponentMessage(input=[1., 2., 3.], health_check=True)
                response = stub.forward(request)
                ic(response.output)
        case 50053 | 50054:
            # Connect to Feeder or Offline Feederservice
            with grpc.insecure_channel(f"localhost:{port}") as channel:
                stub = ComponentStub(channel)
                request = ComponentMessage(input=[])
                response = stub.forward(request)
                ic(response.output)
        case _:
            with grpc.insecure_channel(f"localhost:{port}") as channel:
                stub = ComponentStub(channel)
                request = ComponentMessage(input=[0.], health_check=True)
                response = stub.forward(request)
                ic(response.output)

if __name__ == '__main__':
    main()
