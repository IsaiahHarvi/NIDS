import os
import docker
from threading import Thread

from icecream import ic
ic.configureOutput(includeContext=False, prefix="")

class Logger:
    def __init__(self):
        ic(f"Logger started on port {os.environ.get('PORT')}")
        self.client = docker.from_env()
        self.services = self.get_service_names()
        ic(f"Collecting logs for: {', '.join(self.services)}")
        self.start_log_collection()

    def get_service_names(self):
        try:
            containers = self.client.containers.list()
            services = [
                container.name for container in containers 
                if 'nids-' in container.name 
                and 'logger' not in container.name
            ]
            ic(f"Identified services: {services}")
            return services
        except Exception as e:
            ic(f"Failed to get service names: {e}")
            return []

    def start_log_collection(self):
        threads = []
        for name in self.services:
            thread = Thread(target=self.monitor_logs, args=(name,))
            thread.start()
            threads.append(thread)

        # Join threads to ensure they run indefinitely
        for thread in threads:
            thread.join()

    def monitor_logs(self, name):
        spc = max([len(name) for name in self.services])
        try:
            ic(f"Starting log collection for service: {name}")
            container = self.client.containers.get(name)
            for line in container.logs(stream=True):
                out = f"{name}{' ' * (spc - len(name))}| {line.strip().decode('utf-8')}"
                # ic(out) 
        except Exception as e:
            ic(f"Error occurred while monitoring {name}: {e}")
        except KeyboardInterrupt:
            ic(f"SIGINT received, shutting down {name}...")

if __name__ == "__main__":
    Logger()
