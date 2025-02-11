#!/usr/bin/env bash

# UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# general git config
git config --global --add safe.directory /workspaces/NIDS
git config --global pull.rebase true
git lfs install
git status

# clear all residual docker stuff
docker system prune --volumes -af | true
docker volume rm mongo-data | true

# make mongo service accessible from host
if ! grep -q "# NIDS" /etc/hosts; then
    echo -e "\n# NIDS\n127.0.0.1 mongo" | sudo tee -a /etc/hosts
    echo "NIDS entry added to /etc/hosts"
else
    echo "NIDS entry already exists in /etc/hosts"
fi
