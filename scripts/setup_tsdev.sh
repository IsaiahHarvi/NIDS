#!/usr/bin/env bash

bash scripts/setup_common.sh

pip3 install --no-cache-dir --user -r .devcontainer/requirements-cpu.txt -e .

cd app/client
npm i -g bun && bun i

cd ../../app/server
npm i -g bun && bun i

cd ../..

echo "Done."
