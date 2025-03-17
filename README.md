# NIDS: Real-Time Network Intrusion Detection, Monitoring, and Analysis

[![Version](https://img.shields.io/github/v/release/IsaiahHarvi/NIDS.svg)](https://github.com/IsaiahHarvi/NIDS/releases)
[![Tests Passing](https://img.shields.io/github/actions/workflow/status/IsaiahHarvi/NIDS/publish.yml)](https://github.com/IsaiahHarvi/NIDS/actions?query=workflow%3Atest)
[![GitHub Contributors](https://img.shields.io/github/contributors/IsaiahHarvi/NIDS.svg)](https://github.com/IsaiahHarvi/NIDS/graphs/contributors)
[![Issues](https://img.shields.io/github/issues/IsaiahHarvi/NIDS.svg)](https://github.com/IsaiahHarvi/NIDS/issues)
[![Pull Requests](https://img.shields.io/github/issues-pr/IsaiahHarvi/NIDS.svg)](https://github.com/IsaiahHarvi/NIDS/pulls)
[![Discord](https://img.shields.io/discord/:1276597095138070792)](https://discord.gg/m2TWH5nsAP)

## Overview
**NIDS** is a real-time Network Intrusion Detection System designed to monitor and analyze network traffic. After installation, NIDS acts as a drop-in client on your network. It utilizes Deep Neural Networks to detect malicious attacks by identifying abnormal patterns and generating alerts for potential threats like unauthorized access, data exfiltration, and various types of Denial of Service attacks.

## Architecture
NIDS is deployed on a Linux server connected to the network you want to monitor. It consists of several components:
- **Packet Capture Module**: Continuously captures live network traffic.
- **Detection Engine**: Uses machine learning for threat detection via anomaly and signature-based methods.
- **Logging Service**: Maintains a record of network traffic for future analysis or forensic investigations.
- **Data Visualization Dashboard**: Offers real-time visualizations and historical analysis of network traffic.

Each component runs in its own Docker container, ensuring modularity, scalability, and secure service networking. In case the web interface is inaccessible, a built-in terminal interface is available for management.

## Key Features

### Real-Time Network Traffic Monitoring
- **Packet Capture**: Constant monitoring of live network traffic.
- **Packet Inspection**: Detailed analysis including IP addresses, ports, protocols, etc.
- **Traffic Logging**: Persistent logging for later analysis and forensics.

### Threat Detection with Signature and Anomaly-Based Methods
- **Anomaly-Based Detection**: Leverages machine learning to detect deviations from normal traffic behavior.

### Docker Integration for Service Networking
- **Isolation**: Each service runs in its own container, minimizing cross-service vulnerabilities.
- **Secure Communication**: Docker’s virtualized networking stack secures inter-service communication.
- **Portability**: Consistent deployment across various environments using Docker.

### Data Visualization Dashboard
- **Real-Time Visualizations**: Monitors traffic flow, volume by protocol, and geographic source of traffic.
- **Historical Analysis**: Supports trend analysis with filtering options by time, location, or severity.

## Installation
Follow the [User Guide](./docs/USERGUIDE.md) to install and run NIDS. Installation is streamlined through two scripts that set up the environment and deploy the necessary containers.

## Contributing
Contributions are welcome! Please refer to the [CONTRIBUTING.md](./docs/CONTRIBUTING.md) for guidelines and instructions.

## License
[MIT License](./LICENSE)
