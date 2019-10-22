#!/usr/bin/env bash

# Path to the CUDA binary folder.
CUDA_DIR="/usr/local/cuda-9.1/bin/"

echo "Don't forget to change the working directory!"
sleep 1

# Nvidia visual profiler
${CUDA_DIR}/nvvp "python -m optical_simulation.run_simulation"
