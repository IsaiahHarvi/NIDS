#!/usr/bin/env bash

# general git config
git config --global --add safe.directory /workspaces/NIDS
git config --global pull.rebase false
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

# update and install deps/utils
sudo apt update > /dev/null 2>&1
sudo apt upgrade -y
sudo DEBIAN_FRONTEND=noninteractive apt install -y vim tmux \
    dnsutils iputils-ping curl wget tshark 

# clear all residual docker stuff
docker system prune --volumes -af | true
docker volume rm mongo-data | true

# make mongo service accessible from host
echo "127.0.0.1 mongo" | sudo tee -a /etc/hosts
