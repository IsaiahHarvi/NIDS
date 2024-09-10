import os
import docker
from threading import Thread
from pymongo import MongoClient
from datetime import datetime
from icecream import ic

ic.configureOutput(includeContext=False, prefix="")

class Logger:
    def __init__(self):
        ic(f"Logger started on port {os.environ.get('PORT')}")
        self.client = docker.from_env()
        self.mongo_client = MongoClient("mongodb://root:example@mongo:27017/?replicaSet=rs0")
        self.db = self.mongo_client["logs"]
        self.collection = self.db["log_entries"]

        self.services = self.get_service_names()
        ic(f"Collecting logs for: {', '.join(self.services)}")
        self.start_log_collection()

    def get_service_names(self):
        try:
            containers = self.client.containers.list()
            services = [
                container.name
                for container in containers
                if container.name in ["neural-network", "mongo", "mongo-express", "offline-feeder", "webserver"] and "logger" not in container.name
            ]
            ic(f"Identified services: {services}")
            return services
        except Exception as e:
            ic(f"Failed to get service names: {e}")
            return []

    def start_log_collection(self):
        threads = []
        for name in self.services:
            thread = Thread(target=self.monitor_logs, args=(name,), daemon=True)
            thread.start()
            threads.append(thread)

    def monitor_logs(self, name):
        spc = max([len(name) for name in self.services])
        try:
            ic(f"Starting log collection for service: {name}")
            container = self.client.containers.get(name)
            for line in container.logs(stream=True):
                log_message = line.strip().decode('utf-8', errors='replace')
                out = f"{name}{' ' * (spc - len(name))}| {log_message}"
                
                self.store_log(name, log_message)
        except Exception as e:
            ic(f"Error occurred while monitoring {name}: {e}")
        except KeyboardInterrupt:
            ic(f"SIGINT received, shutting down {name}...")

    def store_log(self, service_name, message):
        try:
            log_entry = {
                "service_name": service_name,
                "message": message,
                "timestamp": datetime.utcnow(),
            }
            self.collection.insert_one(log_entry)
            ic(f"Log stored for {service_name}")
        except Exception as e:
            ic(f"Failed to store log: {e}")


if __name__ == "__main__":
    Logger()
