import grpc
# python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. src/grpc_/services.proto

def start_server(service, port=50051, wait_for_termination: bool = True) -> None | grpc.Server:
    import grpc
    from concurrent import futures
    from src.grpc_.services_pb2_grpc import add_ComponentServicer_to_server
    
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_ComponentServicer_to_server(service, server)
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    print(f"Service {service.__class__.__name__} started on port {port}")

    if wait_for_termination: # flag for unit tests
        server.wait_for_termination()
    else:
        return server
