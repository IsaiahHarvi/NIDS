#!/usr/bin/env bash

git lfs install
git config --global --add safe.directory /workspaces/CS-499
git config --global pull.rebase false

# docker container prune -f | true
# docker image prune -f | true
# docker volume prune -f --all | true
docker system prune --volumes -af | true

sudo apt update > /dev/null 2>&1 && sudo apt upgrade -y
sudo apt install -y vim tmux neovim fzf \
    dnsutils iputils-ping curl tshark wget
