#!/bin/sh
set -e

curl -LsSf https://astral.sh/uv/install.sh | sh

echo 'export PATH="$HOME/.local/bin:$PATH"' >> /etc/bash.bashrc
echo 'export PATH="$HOME/.local/bin:$PATH"' >> /etc/zsh/zshrc
. $HOME/.local/bin/env || true

# uv pip compile requirements-cpu.in \
    # --output-file requirements-cpu.txt

if [ "${GPU}" = "true" ]; then
    uv pip sync --system requirements.txt
else
    uv pip sync --system requirements-cpu.txt
fi
