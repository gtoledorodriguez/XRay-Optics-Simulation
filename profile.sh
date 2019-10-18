#!/usr/bin/env bash

conda activate agis

nvprof python -m optical_simulation.run_simulation
