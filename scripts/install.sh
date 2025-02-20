#!/usr/bin/env bash

command_exists() {
    command -v "$1" &> /dev/null
}

if ! grep -q "# NIDS" /etc/hosts; then
    echo -e "\n# NIDS\n127.0.0.1 mongo" | sudo tee -a /etc/hosts
    echo "NIDS entry added to /etc/hosts"
else
    echo "NIDS entry already exists in /etc/hosts"
fi

# Confirm before running the pip command
echo "Do you want to install the Graphical Terminal Interface? (y/n)"
read -r confirm_install

if [[ "$confirm_install" == "y" ]]; then
    if ! command -v uv &> /dev/null; then
        echo "'uv' is not installed. Installing uv..."
        pip3 install --user uv
    fi
    uv pip install --no-cache-dir --user .
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

echo "Successfully installed NIDS."

echo "Run with ./scripts/deploy.sh"
