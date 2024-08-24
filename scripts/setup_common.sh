#!/usr/bin/env bash

rm setup.err setup.log 2> /dev/null

# Setup git
git config --global --add safe.directory /workspaces/CS-499
git config --global pull.rebase false

# or true to ignore errors when there aren't containers or dangling images
docker container prune -f | true
docker image prune -f | true
docker volume prune -f --all | true
# docker system prune --volumes -af | true

sudo apt update && sudo apt upgrade -y
sudo apt install -y vim tmux neovim fzf dnsutils iputils-ping curl
