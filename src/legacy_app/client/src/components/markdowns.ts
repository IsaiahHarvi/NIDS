// markdowns.ts
export const userGuide = `
NIDS: Operator Manual

Table of Contents  
1. Introduction  
2. Installation  
3. Usage  
4. Troubleshooting  

Introduction  
This document provides an overview of the NIDS operator manual. It includes information on how to install, configure, and use the NIDS service.  
Ideally, NIDS is meant to be run on a server that is connected to a network that you would like to monitor. NIDS hosts a web interface that allows users to view network traffic and alerts in real-time. If for any reason the web interface is not accessible, the NIDS service can still be managed via the terminal interface.

Installation  
Note that NIDS is designed to run on a Linux-based system. It also functions without regard to any other docker services and will not hesitate to remove them. Adjust your installation environment accordingly.

To install NIDS, follow the steps below:  
1. Clone the repository to a preferred directory:  
\`git clone https://github.com/IsaiahHarvi/NIDS.git\`  
2. Navigate to the NIDS directory:  
\`cd NIDS\`  
3. Run Install script:  
\`./scripts/install.sh\`  
This will install any needed dependencies.

Usage  
To use NIDS, follow the steps below:  
1. Ensure you are in the NIDS directory:  
\`cd /path/to/NIDS\`  
2. Start the NIDS service:  
\`./scripts/deploy.sh\`  
3. Access the web interface by navigating to \`http://localhost:5000\` in your preferred web browser.  
The web interface provides a visual representation of network traffic and alerts in real-time as well as the ability to manage the NIDS service.  
4. Access the terminal interface by running:  
\`python3 scripts/display.py\`  
The terminal interface provides direct control over the NIDS service. It is useful for managing the service when the web interface is not accessible. But currently does not provide monitoring tools.

Troubleshooting  
If you encounter any issues with the NIDS service, please refer to the following troubleshooting steps:  
1. Uninstall  
\`./scripts/uninstall.sh\`  
2. Reinstall & Run  
\`./scripts/install.sh\`  
\`./scripts/deploy.sh\`
`;

export const mainReadMe = `
NIDS: Real-Time Network Intrusion Detection, Monitoring, and Analysis

Overview  
NIDS is a real-time Network Intrusion Detection System designed to monitor and analyze network traffic. After installation, NIDS is just another client on a network, allowing it to be a drop-in service. It utilizes Deep Neural Networks to detect malicious attacks by identifying abnormal patterns and generating alerts for potential threats such as unauthorized access, data exfiltration, and various types of Denial of Service attacks. The user guide is available [here](./docs/USERGUIDE.md).

Architecture  
The following diagram illustrates a high-level overview of the NIDS system. NIDS is intended to be ran on a Linux server connected to the network that you would like to monitor. The system consists of several components, including a packet capture module, a detection engine, a logging service, and a data visualization dashboard. The system is designed to be modular and scalable, allowing for easy integration with other security tools and services. It can be accessed via a web-based dashboard for real-time management, monitoring, and analysis of network traffic. NIDS also has a built-in terminal interface for management if the web interface is not accessible.

The Feeder service is the only part of NIDS that is on the host network.

Key Features  

Real-Time Network Traffic Monitoring  
- Packet Capture: Continuously monitors live network traffic on the host's network.  
- Deep Packet Inspection: Analyzes captured packets for detailed information, including IP addresses, ports, protocols, and more.  
- Traffic Logging: Stores logs of network traffic for future analysis or forensic investigations.  

Threat Detection with Signature and Anomaly-Based Methods  
- Anomaly-Based Detection: Utilizes machine learning to detect abnormal behavior in network traffic that deviates from baseline patterns (e.g., unusual data transfer volumes).  

Intrusion Detection Alerts and Reporting  
- Real-Time Alerts: Generates alerts when suspicious activity is detected.  
- Threat Classification: Classifies detected intrusions by severity (low, medium, high), based on the type and potential impact of the threat.  
- Incident Reporting: Automatically generates reports on detected threats, including time of detection, type of threat, and affected network segment.  

Docker Integration for Service Networking  
- Service Isolation: Each service within NIDS (e.g., packet capture, logging, detection engine) runs in its own container, reducing the risk of cross-service vulnerabilities and ensuring potential security issues in one service don't affect others.  
- Secure Service Networking: Docker’s virtualized networking stack ensures secure communication between NIDS components without directly exposing them to the host network.  
- Enhanced Security: Docker’s containerization limits exposure by isolating services from the host system and one another, reducing the overall attack surface.  
- Portability: Docker ensures NIDS can be deployed consistently across different environments, maintaining uniform behavior and configuration.  

Data Visualization Dashboard  
- Traffic Visualizations: Provides real-time visualizations of network traffic, including traffic flow, volume by protocol, and geographic source of traffic.  
- Threat Maps: Displays an interactive threat map showing the source and destination of potential attacks, along with their severity.  
- Historical Analysis: Allows users to view historical trends in network traffic and threats, with filtering options by time, location, or severity.  

API for Security Integration  
- REST API: Exposes functionality through an API, enabling external systems to retrieve traffic logs.  
- Custom Integration: Provides flexibility for security teams to integrate with other enterprise systems (e.g., firewalls, intrusion prevention systems) and customize response actions and alerts.  

Team Distribution  
- Casey Bramlett: Front End Lead  
- Isaiah Harville:  
  - Technical Lead  
  - Machine Learning Specialist  
- Jacob Neel: Back End Developer  
- Kevin Santschi: Back End Developer
`;

export const aiReadMe = `
Training Anomaly Models for NIDS Integration

This document explains how to train Network Intrusion Detection System (NIDS) models for modular integration in our ML-based product. It includes details about the required setup, feature generation, checkpoints, and integration with the neural network service. By following this guide, you can train and integrate NIDS models efficiently while maintaining modularity and compatibility with our product's neural network service.

---

1. Overview  

Our NIDS module is designed for modularity and flexibility. Our training pipeline processes network traffic data, generates statistical features, and trains machine learning models to detect anomalies and intrusions. The trained models can be integrated seamlessly into our neural network service for deployment.

---

2. Key Components  

a. Feature Generation Using NFStream  
We utilize NFStream for network traffic feature generation. NFStream extracts statistical and flow-based features from packet capture (PCAP) files. These features are essential for training and include:  
- Flow statistics: Byte and packet counts, duration, and rates.  
- Protocol analysis: Flags and type-based distributions.  
- Statistical measures: Min, max, mean, and standard deviation of inter-packet arrival times.  

The features are preprocessed using standard scaling and fed into the training pipeline. Ensure your data adheres to this structure.

b. Checkpoints and Model Integration  
- Checkpoints Directory:  
  - Store trained model checkpoints in the \`data/checkpoints\` directory.  
  - Checkpoint files should be named clearly to indicate the model type, date, and version (e.g., \`mlp_nids_v1_2024-12-01.ckpt\`).  

- Parameterization in Neural Network Service:  
  - Define the path to the checkpoint in the neural network service configuration. This ensures the correct model is loaded during deployment.  
  - Example configuration parameter:  
    \`\`\`yaml
    model_checkpoint: "data/checkpoints/mlp_nids_v1_2024-12-01.ckpt"
    \`\`\`

---

3. Training Pipeline  

a. Dataset Preparation  
1. Collect network traffic in PCAP format and preprocess it using NFStream to extract statistical features.  
2. Ensure class labels are clean, balanced, and merged appropriately. For instance, combine similar classes (e.g., \`portscan\` and \`port_scan\`) to maintain consistency.

b. Model Training Steps  
1. Set Up Environment:  
   - Ensure dependencies are installed:  
     \`\`\`bash
     pip install -r requirements.txt
     \`\`\`  
   - Include necessary tools such as PyTorch, Lightning, Pandas, and NFStream.  

2. Prepare the Data Module:  
   - Define paths to input data.  
   - Use stratified sampling for train-test splits.  
   - Apply undersampling and oversampling strategies to balance classes as needed.  

3. Train the Model:  
   - Use the \`train.py\` script to initiate the training:  
     \`\`\`bash
     python train.py --lr 0.001 --batch_size 64 --early_stop_patience 10 --ckpt_name nids_model --constructor MLP --all_data
     \`\`\`

4. Monitor Training:  
   - Track training and validation metrics using tools like WandB.  

5. Save Checkpoints:  
   - Store the best-performing model checkpoint in \`data/checkpoints\`.

---

4. Best Practices  

Modularity  
- Use parameterized configurations for paths and model parameters to make the system modular and reusable.  
- Ensure all key components are decoupled, e.g., feature extraction, model training, and evaluation.

Feature Engineering  
- Features from NFStream are the core input for our models. Avoid adding unsupported features to ensure compatibility with the existing pipeline.

Reproducibility  
- Always log hyperparameters, seed values, and configurations to replicate results effectively.

---

5. Integration Checklist  

1. Ensure the checkpoint file is placed in \`data/checkpoints\`.  
2. Verify that the feature generation pipeline outputs are compatible with the model's input layer.  
3. Parameterize the checkpoint path in the neural network service configuration.  
4. Test the trained model's performance on a validation set before deployment.
`;
