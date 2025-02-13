#!/usr/bin/env python3
import json
import os
import platform
import subprocess
import sys

"""Trusts the locally hosted insecure docker registry. Requires elevated permissions."""

def update_daemon_config(file_path, registry):
    config = {}
    if os.path.exists(file_path):
        try:
            with open(file_path, "r") as f:
                config = json.load(f)
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            return False

    insecure_registries = config.get("insecure-registries", [])
    if registry not in insecure_registries:
        insecure_registries.append(registry)
    config["insecure-registries"] = insecure_registries

    try:
        with open(file_path, "w") as f:
            json.dump(config, f, indent=2)
    except Exception as e:
        print(f"Error writing to {file_path}: {e}")
        return False

    print(f"Updated {file_path} with insecure registry: {registry}")
    return True

def restart_docker(os_type):
    try:
        if os_type == "Linux":
            print("Restarting Docker service on Linux...")
            subprocess.run(["systemctl", "restart", "docker"], check=True)
        elif os_type == "Windows":
            print("Restarting Docker service on Windows...")
            subprocess.run(["powershell", "-Command", "Restart-Service docker"], check=True)
        elif os_type == "Darwin":
            print("Restarting Docker Desktop on macOS...")
            # Quit and re-open Docker Desktop (requires Docker Desktop to be installed in /Applications)
            subprocess.run(["osascript", "-e", 'quit app "Docker"'], check=True)
            subprocess.run(["open", "-a", "Docker"], check=True)
        else:
            print("Please restart Docker.")
    except subprocess.CalledProcessError as e:
        print(f"Error restarting Docker: {e}")

def main():
    registry = "172.17.0.1:42069"
    os_type = platform.system()
    print(f"Detected OS: {os_type}")

    if os_type == "Linux":
        daemon_file = "/etc/docker/daemon.json"
    elif os_type == "Windows":
        daemon_file = r"C:\ProgramData\Docker\config\daemon.json"
    elif os_type == "Darwin":
        daemon_file = "/etc/docker/daemon.json"
        if not os.path.exists(daemon_file):
            print(f"{daemon_file} does not exist. For Docker Desktop on macOS, please update settings via Docker Desktop preferences.")
            sys.exit(1)
    else:
        print("Unsupported operating system.")
        sys.exit(1)

    if update_daemon_config(daemon_file, registry):
        restart_docker(os_type)
    else:
        print("Failed to update Docker daemon configuration.")

if __name__ == "__main__":
    main()
