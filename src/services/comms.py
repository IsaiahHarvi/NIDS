"""
Simple method to interact with the gRPC services oustide of the test suite.
"""
import click
import grpc
from src.grpc_.services_pb2 import ComponentMessage
from src.grpc_.services_pb2_grpc import ComponentStub

from icecream import ic


@click.command()
@click.option('--port', default=50053, help='Port of the service to connect to.')
def main(port):
    match port:
        case 50051:
            # Connect to Recurrent service
            with grpc.insecure_channel('localhost:50051') as channel:
                stub = ComponentStub(channel)
                request = ComponentMessage(input=[1., 2., 3.], health_check=True)
                response = stub.forward(request)
                ic(response.output)
        case 50052:
            # Connect to Residual service
            with grpc.insecure_channel('localhost:50052') as channel:
                stub = ComponentStub(channel)
                request = ComponentMessage(input=[1., 2., 3.], health_check=True)
                response = stub.forward(request)
                ic(response.output)
        case 50053:
            # Connect to Residual service
            with grpc.insecure_channel('localhost:50053') as channel:
                stub = ComponentStub(channel)
                request = ComponentMessage(input=[])
                response = stub.forward(request)
                ic(response.output)

if __name__ == '__main__':
    main()