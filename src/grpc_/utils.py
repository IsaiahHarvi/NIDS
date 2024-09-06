# python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. src/grpc_/services.proto

import time 
import subprocess
import grpc
from concurrent import futures

from src.grpc_.services_pb2 import ComponentMessage, ComponentResponse
from src.grpc_.services_pb2_grpc import ComponentStub
from src.grpc_.services_pb2_grpc import add_ComponentServicer_to_server

from icecream import ic


def start_server(
    service, port, wait_for_termination: bool = True
) -> None | grpc.Server:
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10),
        options=[
            ('grpc.max_send_message_length', 50 * 1024 * 1024),  # 50 MB
            ('grpc.max_receive_message_length', 50 * 1024 * 1024)  # 50 MB
        ]
    )
    add_ComponentServicer_to_server(service, server)
    server.add_insecure_port(f"[::]:{port}")
    server.start()
    print(f"Service {service.__class__.__name__} started on port {port}")

    if wait_for_termination:  # flag for unit tests
        server.wait_for_termination()
    else:
        return server

def wait_for_services(services: list, timeout=60, init_time=5):
    """
    Wait for the specified services to appear in `docker ps`.
    """
    start_time = time.time()
    while (time.time() - start_time) < timeout:
        output = subprocess.check_output(["docker", "ps"], text=True)
        if all(service in output for service in services):
            time.sleep(init_time)
            return
        time.sleep(1)

    raise RuntimeError(f"Services did not start within {timeout} seconds: {services}")

def sendto_service(msg: ComponentMessage, host: str, port: int) -> ComponentResponse:
    ic("Sending data to", host, port)
    try:
        with grpc.insecure_channel(
            f"{host}:{port}",
            options=[
                ('grpc.max_send_message_length', 50 * 1024 * 1024),  # 50 MB
                ('grpc.max_receive_message_length', 50 * 1024 * 1024)  # 50 MB
            ]
        ) as channel:
            response = ComponentStub(channel).forward(msg)
            return response
    except Exception as e:
        ic("Send Failed", e)

def sendto_mongo(data: dict, collection_name: str) -> None:
    from pymongo import MongoClient # not all services use this, so import here

    client = MongoClient("mongodb://root:example@mongo:27017/?replicaSet=rs0")
    db = client["store_service"]
    collection = db[collection_name]
    result = collection.insert_one(data)
    ic(result.inserted_id)
