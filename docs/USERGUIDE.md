# NIDS: Operator Manual

## Table of Contents
1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Usage](#usage)
4. [Troubleshooting](#troubleshooting)

## Introduction
This document provides an overview of the NIDS operator manual. It includes information on how to install, configure, and use the NIDS service.
Ideally, NIDS is meant to be run on a server that is connected to a network that you would like to monitor. NIDS hosts a web interface that allows users to view network traffic and alerts in real-time. If for any reason the web interface is not accessible, the NIDS service can still be managed via the  terminal interface.

## Installation
Note that NIDS is designed to run on a Linux-based system. It also functions without regard to any other docker services and will not hesistate to remove them. Adjust your installation environment accordingly.

To install NIDS, follow the steps below:
1. Clone the repository to a preferred directory:
```
git clone https://github.com/IsaiahHarvi/NIDS.git
```
2. Navigate to the NIDS directory:
```
cd NIDS
```
3. Run Install script:
```
./scripts/install.sh
```
> This will install any needed dependencies.

## Usage
To use NIDS, follow the steps below:
1. Ensure you are in the NIDS directory:
```
cd /path/to/NIDS
```
2. Start the NIDS service:
```
./scripts/deploy.sh
```
3. Access the web interface by navigating to `http://localhost:5000` in your preferred web browser.
> The web interface provides a visual representation of network traffic and alerts in real-time as well as the ability to manage the NIDS service.
4. Access the terminal interface by running:
```
python3 scripts/display.py
```
> The terminal interface provides direct control over the NIDS service. It is useful for managing the service when the web interface is not accessible. But currently does not provide monitoring tools.

## Troubleshooting
If you encounter any issues with the NIDS service, please refer to the following troubleshooting steps:
1. Uninstall
```
./scripts/uninstall.sh
```
2. Reinstall & Run
```
./scripts/install.sh
./scripts/deploy.sh
```
