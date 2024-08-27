#!/usr/bin/env bash

bash scripts/setup_devcontainer.sh

cd app/client

npm i -g bun
bun i 
