#!/usr/bin/env bash

source ./options.sh # Include file.

echo "Don't forget to change the working directory!"
sleep 1

# Nvidia visual profiler
${CUDA_DIR}/nvvp "python -m optical_simulation.run_simulation"
