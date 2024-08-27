#!/usr/bin/env bash

bash scripts/setup_devcontainer.sh

bun i 
npm i -g bun

cd app/client
