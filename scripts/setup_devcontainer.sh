#! /bin/bash -e

bash ./scripts/setup_common.sh

pip3 install --no-cache-dir --user -r .devcontainer/requirements.txt -e .

