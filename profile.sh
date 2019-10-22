#!/usr/bin/env bash

# Path to the CUDA binary folder.
CUDA_DIR="/usr/local/cuda-9.1/bin/"

# Nvidia command-line profiler
${CUDA_DIR}/nvprof python -m optical_simulation.run_simulation
