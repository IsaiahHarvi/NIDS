#!/usr/bin/env bash

docker container prune -y
docker image prune -y
docker volume prune -y

sudo apt update && sudo apt upgrade -y
sudo apt install -y vim tmux neovim fzf dnsutils iputils-ping curl

# Setup git
git config --global --add safe.directory /workspaces/CS-499
git config --global pull.rebase false