#!/usr/bin/env bash

source ./options.sh # Include file.

echo "Use these settings for nvvp:"
echo "Toolkit/Script: CUDA Toolkit 9.1 (/usr/local/cuda-9.1/bin/)"
echo "File: /home/YOUR_USERNAME/miniconda3/envs/agis/bin/python3.7"
echo "Working directory: /home/YOUR_USERNAME/GitHub/Antimatter-Gravity-Interferometer-Simulation/"
echo "Arguments: '-m optical_simulation.run_simulation'"

sleep 3

# Nvidia visual profiler
${CUDA_DIR}/nvvp "python -m optical_simulation.run_simulation"
