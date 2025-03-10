# NIDS: Real-Time Network Intrusion Detection, Monitoring, and Analysis

## Contributing
For information on contributing to this project, please see the [CONTRIBUTING.md](./docs/CONTRIBUTING.md) file.

## Overview
**NIDS** is a real-time Network Intrusion Detection System designed to monitor and analyze network traffic. After installation, NIDS is just another client on a network, allowing it to be a drop-in service. It utilizes Deep Neural Networks to detect malicious attacks by identifying abnormal patterns and generating alerts for potential threats such as unauthorized access, data exfiltration, and various types of Denial of Service attacks. The user guide is available [here](./docs/USERGUIDE.md)

### Architecture
NIDS is intended to be ran on a linux server connected to the network that you would like to monitor. The system consists of several components, including a packet capture module, a detection engine, a logging service, and a data visualization dashboard. The system is designed to be modular and scalable, allowing for easy integration with other security tools and services. It can be accessed via a web-based dashboard for real-time management, monitoring and analysis of network traffic. NIDS also has a built-in terminal interface for management if the web interface is not accessible.

>There is an excalidraw diagram under `docs/` that shows the architecture of the system.

## Key Features

### Real-Time Network Traffic Monitoring
- **Packet Capture**: Continuously monitors live network traffic on the host's network.
- **Deep Packet Inspection**: Analyzes captured packets for detailed information, including IP addresses, ports, protocols, and more.
- **Traffic Logging**: Stores logs of network traffic for future analysis or forensic investigations.

### Threat Detection with Signature and Anomaly-Based Methods
- **Anomaly-Based Detection**: Utilizes machine learning to detect abnormal behavior in network traffic that deviates from baseline patterns (e.g., unusual data transfer volumes).

### Docker Integration for Service Networking
- **Service Isolation**: Each service within NIDS (e.g., packet capture, logging, detection engine) runs in its own container, reducing the risk of cross-service vulnerabilities and ensuring potential security issues in one service don't affect others.
- **Secure Service Networking**: Docker’s virtualized networking stack ensures secure communication between NIDS components without directly exposing them to the host network.
- **Enhanced Security**: Docker’s containerization limits exposure by isolating services from the host system and one another, reducing the overall attack surface.
- **Portability**: Docker ensures NIDS can be deployed consistently across different environments, maintaining uniform behavior and configuration.

### Data Visualization Dashboard
- **Traffic Visualizations**: Provides real-time visualizations of network traffic, including traffic flow, volume by protocol, and geographic source of traffic.
- **Threat Maps**: Displays an interactive threat map showing the source and destination of potential attacks, along with their severity.
- **Historical Analysis**: Allows users to view historical trends in network traffic and threats, with filtering options by time, location, or severity.

### API for Security Integration
- **REST API**: Exposes functionality through an API, enabling external systems to retrieve traffic logs <!--, send alerts to a SIEM, or integrate with a Security Orchestration, Automation, and Response (SOAR) platform. -->
- **Custom Integration**: Provides flexibility for security teams to integrate with other enterprise systems (e.g., firewalls, intrusion prevention systems) and customize response actions and alerts.
