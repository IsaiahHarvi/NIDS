#!/usr/bin/env bash

# NOTE: This is for use in a production environment on a Linux machine.

command_exists() {
    command -v "$1" &> /dev/null
}


if ! grep -q "# NIDS" /etc/hosts; then
    echo -e "\n# NIDS\n127.0.0.1 mongo" | sudo tee -a /etc/hosts
    echo "NIDS entry added to /etc/hosts"
else
    echo "NIDS entry already exists in /etc/hosts"
fi

# Install Docker if not installed
if ! command_exists docker; then
    echo "Docker not found. Installing Docker..."
    
    sudo apt-get update
    sudo apt-get install -y \
        ca-certificates \
        curl \
        gnupg \
        lsb-release \
        xdg-utils
    
    # Add Docker’s official GPG key
    sudo mkdir -p /etc/apt/keyrings
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
    
    # Set up the stable Docker repository
    echo \
    "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
    $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    
    # Install and Start Docker
    sudo apt-get update
    sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

    if ! command_exists docker; then
        echo "Docker installation failed."
        exit 1
    fi

    sudo systemctl start docker
    sudo systemctl enable docker
fi

# Install Docker Compose if not installed
if ! command_exists docker-compose; then
    echo "Docker Compose not found. Installing Docker Compose..."
    
    sudo curl -L "https://github.com/docker/compose/releases/download/v2.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
    
    if ! command_exists docker-compose; then
        echo "Docker Compose installation failed."
        exit 1
    fi
fi

echo "Docker is Ready."

# Start NIDS
docker-compose --profile feeder --profile gui down # stop any running services, just in case

echo "-------------------------------------------------------------------"
echo "Starting Services..."

docker-compose -f compose.yml up -d webserver # bring up just the webserver
echo -e "\nView GUI at http://localhost:8000"
if command_exists xdg-open; then
    xdg-open http://localhost:8000 & > /dev/null 2>&1
fi

docker-compose --profile feeder --profile gui up
