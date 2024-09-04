#!/usr/bin/env bash

BASE_DIR="deploy"
for dir in "$BASE_DIR"/*/; do
    find "$dir" -maxdepth 1 -name "*.in" | while read -r infile; do
        echo "Compiling $infile..."
        pip-compile "$infile" # -v
    done
done
