#!/usr/bin/env bash

# Path to the CUDA binary folder.
CUDA_DIR="/usr/local/cuda-9.1/bin/"

if ! [[ -d ${CUDA_DIR} ]]; then
    echo "'${CUDA_DIR}' does not exist. Falling back to '/usr/bin/'."
    CUDA_DIR="/usr/bin/"
fi