#!/usr/bin/env bash

# general git config
git config --global --add safe.directory /workspaces/NIDS
git config --global pull.rebase true

# clear all residual docker stuff
docker volume rm mongo-data | true

# make mongo service accessible from host
if ! grep -q "# NIDS" /etc/hosts; then
    echo -e "\n# NIDS\n127.0.0.1 mongo" | sudo tee -a /etc/hosts
    echo "NIDS entry added to /etc/hosts"
else
    echo "NIDS entry already exists in /etc/hosts"
fi

curl -LsSf https://astral.sh/uv/install.sh | sh

echo 'export PATH="$HOME/.local/bin:$PATH"'

if command -v nvidia-smi &> /dev/null; then
    uv pip install --system --index-strategy unsafe-best-match \
        --extra-index-url https://download.pytorch.org/whl/cu124 \
        -r .devcontainer/requirements.txt
else
    uv pip install --system --index-strategy unsafe-best-match \
        --extra-index-url https://download.pytorch.org/whl/cpu \
        -r .devcontainer/requirements-cpu.txt
fi

uv pip install -e .
