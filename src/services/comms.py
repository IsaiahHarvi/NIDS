"""
Simple method to interact with the gRPC services oustide of the test suite.
"""
import grpc
from src.grpc_.services_pb2 import ComponentMessage
from src.grpc_.services_pb2_grpc import ComponentStub

from icecream import ic


def main():
    # Connect to Recurrent service on port 50051
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = ComponentStub(channel)
        request = ComponentMessage(input=[1., 2., 3.], health_check=True)
        response = stub.forward(request)

        ic(response.output)

    # Connect to Residual service on port 50052
    with grpc.insecure_channel('localhost:50052') as channel:
        stub = ComponentStub(channel)
        request = ComponentMessage(input=[1., 2., 3.], health_check=True)
        response = stub.forward(request)

        ic(response.output)


if __name__ == '__main__':
    main()