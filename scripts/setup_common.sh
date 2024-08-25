#!/usr/bin/env bash

if [ -f "scripts/setup_git.personal.sh" ]; then
    bash scripts/setup_git.personal.sh
else
    echo -e "\n\n------------------------------------------------------------------------"
    echo -e "WARNING: setup_git.personal.sh not found, skipping.\nPlease create this file to streamline your git setup.\nSee scripts/setup_git.sh"
    echo -e "------------------------------------------------------------------------\n\n"
    sleep 5
fi

git config --global --add safe.directory /workspaces/CS-499
git config --global pull.rebase false

sudo apt update > /dev/null 2>&1 && sudo apt upgrade -y
sudo DEBIAN_FRONTEND=noninteractive apt install -y vim tmux neovim fzf \
    dnsutils iputils-ping curl tshark argus-client argus-server wget

git lfs install
git status
# docker container prune -f | true
# docker image prune -f | true
# docker volume prune -f --all | true
docker system prune --volumes -af | true


echo "Bringing up Services"
docker compose up -d