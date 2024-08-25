#!/usr/bin/env bash

if command -v nvidia-smi &> /dev/null; then
    echo -e "\n\nInstalling GPU requirements"
    pip3 install --no-cache-dir --user -r .devcontainer/requirements.txt -e .
else
    echo -e "\n\nNo NVIDIA GPU found... installing CPU requirements."
    pip3 install --no-cache-dir --user -r .devcontainer/requirements-cpu.txt -e .
fi

bash ./scripts/setup_common.sh

echo "Done."
