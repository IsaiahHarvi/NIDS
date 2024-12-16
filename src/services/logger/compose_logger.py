import datetime
import os
import threading

import docker
from icecream import ic
from pymongo import MongoClient

ic.configureOutput(includeContext=False, prefix="")

class Logger:
    def __init__(self):
        # Delete any existing collections in logs database

        ic(f"Logger started on port {os.environ.get('PORT')}")
        self.client = docker.from_env()
        self.mongo_client = MongoClient("mongodb://root:example@mongo:27017/?replicaSet=rs0")
        self.db = self.mongo_client["logs"]
        self.log_lock = threading.Lock()
        self.threads = []

        self.services = self.get_service_names()
        ic(f"Collecting logs for: {', '.join(self.services)}")
        self.start_log_collection()

    def get_service_names(self):
        try:
            containers = self.client.containers.list()
            services = [
                container.name
                for container in containers
                if container.name in [
                    "neural-network",
                    "mongo",
                    "mongo-express",
                    "offline-feeder",
                    "webserver"
                ]
                and "logger" not in container.name
            ]
            ic(f"Identified services: {services}")
            return services
        except Exception as e:
            ic(f"Failed to get service names: {e}")
            return []

    def start_log_collection(self):
        for name in self.services:
            thread = threading.Thread(target=self.monitor_logs, args=(name,))
            thread.start()
            self.threads.append(thread)

    def monitor_logs(self, name):
        spc = max([len(name) for name in self.services])
        try:
            ic(f"Starting log collection for service: {name}")
            container = self.client.containers.get(name)
            for line in container.logs(stream=True):
                out = f"{name}{' ' * (spc - len(name))}| {line.strip().decode('utf-8')}"
                ic(out)
        except Exception as e:
            with self.log_lock:
                ic(f"Error occurred while monitoring {name}: {e}")
        except KeyboardInterrupt:
            with self.log_lock:
                ic(f"SIGINT received, shutting down {name}...")

    def store_log(self, service_name, message):
        try:
            collection = self.db[service_name]
            log_entry = {
                "service_name": service_name,
                "message": message,
                "timestamp": datetime.utcnow(),
            }
            collection.insert_one(log_entry)
            ic(f"Log stored for {service_name} in collection {service_name}")
        except Exception as e:
            with self.log_lock:
                ic(f"Failed to store log: {e}")

    def stop_log_collection(self):
        for thread in self.threads:
            thread.join()

if __name__ == "__main__":
    logger = None
    try:
        logger = Logger()
    except KeyboardInterrupt:
        ic("Shutting down logger...")
        if logger:
            logger.stop_log_collection()
