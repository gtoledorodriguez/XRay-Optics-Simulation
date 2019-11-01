#!/usr/bin/env bash

echo "This file runs a series of tests that vary the amount of source points per slit to see how runtime and memory \
usage will vary when increasing the number of source points."

OUT_DIR="out/gpu-memory-tests/"
OUT_CSV="out/gpu-memory-test.csv"

source ./options.sh # Include file.
mkdir -p ${OUT_DIR}

# List of point sources to try
POINTSOURCES=(100 200 300)

# Generate results
for (( i = 0; i < ${#POINTSOURCES[@]}; ++i )); do
    numpointsource=${POINTSOURCES[i]}

    OUT_FILENAME="${OUT_DIR}/${numpointsource}-point-source.txt"

    if [[ ! -f ${OUT_DIR}/${numpointsource}-point-source.txt ]]; then
        echo "Have not run GPU memory test for ${numpointsource} point sources yet. Running..."

        ${CUDA_DIR}/nvprof python -m optical_simulation.run_simulation --numOfPointSources ${numpointsource} > ${OUT_FILENAME} 2>&1
    else
        echo "Already run GPU memory test for ${numpointsource} point sources. Skipping. Delete file at ${OUT_FILENAME} to run again."
    fi

done

# From results, generate CSV file
echo "Generating CSV file at ${OUT_CSV}"
for f in ${OUT_DIR}/*-point-source.txt; do
    echo ${f}
    cat ${f} | grep "total time:" | head -1
    cat ${f} | grep "mem-to-gpu time:" | head -1
    cat ${f} | grep "kernel time:" | head -1
done
