#!/usr/bin/env bash

bash ./scripts/setup_common.sh

if command -v nvidia-smi &> /dev/null; then
    echo "Installing GPU requirements"
    pip3 install --no-cache-dir --user -r .devcontainer/requirements.gpu.txt -e .
else
    echo "No NVIDIA GPU found... installing CPU requirements."
    pip3 install --no-cache-dir --user -r .devcontainer/requirements-cpu.txt -e .
fi
