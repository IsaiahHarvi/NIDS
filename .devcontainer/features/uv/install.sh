#!/bin/sh
set -e

curl -LsSf https://astral.sh/uv/install.sh | sh

echo 'export PATH="$HOME/.local/bin:$PATH"' >> /etc/bash.bashrc
echo 'export PATH="$HOME/.local/bin:$PATH"' >> /etc/zsh/zshrc
. $HOME/.local/bin/env || true

# uv pip compile requirements-cpu.in \
    # --output-file requirements-cpu.txt

if [ "${GPU}" = "true" ]; then
    uv pip install --system --index-strategy unsafe-best-match \
        --extra-index-url https://download.pytorch.org/whl/cu124 \
        -r requirements.txt
else
    uv pip install --system --index-strategy unsafe-best-match \
        --extra-index-url https://download.pytorch.org/whl/cpu \
        -r requirements-cpu.txt
fi
