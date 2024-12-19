#!/usr/bin/env bash

# UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# general git config
git config --global --add safe.directory /workspaces/NIDS
git config --global pull.rebase true
git lfs install
git status

# personal git config if available
if [ -f "scripts/setup_git_personal.sh" ]; then
    bash scripts/setup_git_personal.sh
else
    echo -e "\n\n------------------------------------------------------------------------"
    echo -e "WARNING: setup_git_personal.sh not found, skipping.\nOptionally create this file to streamline your git setup.\nSee scripts/setup_git.sh"
    echo -e "------------------------------------------------------------------------\n\n"
    sleep 5
fi

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
