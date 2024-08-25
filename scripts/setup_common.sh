#!/usr/bin/env bash

git config --global --add safe.directory /workspaces/NIDS
git config --global pull.rebase false
git lfs install

if [ -f "scripts/setup_git_personal.sh" ]; then
    bash scripts/setup_git_personal.sh
else
    echo -e "\n\n------------------------------------------------------------------------"
    echo -e "WARNING: setup_git_personal.sh not found, skipping.\nPlease create this file to streamline your git setup.\nSee scripts/setup_git.sh"
    echo -e "------------------------------------------------------------------------\n\n"
    sleep 5
fi

sudo apt update > /dev/null 2>&1 && sudo apt upgrade -y
sudo DEBIAN_FRONTEND=noninteractive apt install -y vim tmux \
    dnsutils iputils-ping curl tshark argus-client argus-server wget

# docker container prune -f | true
# docker image prune -f | true
# docker volume prune -f --all | true
docker system prune --volumes -af | true

git status
