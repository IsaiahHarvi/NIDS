import grpc

# python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. src/grpc_/services.proto


def start_server(
    service, port, wait_for_termination: bool = True
) -> None | grpc.Server:
    import grpc
    from concurrent import futures
    from src.grpc_.services_pb2_grpc import add_ComponentServicer_to_server

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
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
    import time, subprocess

    start_time = time.time()
    while (time.time() - start_time) < timeout:
        output = subprocess.check_output(["docker", "ps"], text=True)
        if all(service in output for service in services):
            time.sleep(init_time)
            return
        time.sleep(1)

    raise RuntimeError(f"Services did not start within {timeout} seconds: {services}")
