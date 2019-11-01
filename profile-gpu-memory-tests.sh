#!/usr/bin/env bash

echo "This file runs a series of tests that vary the amount of source points per slit to see how runtime and memory \
usage will vary when increasing the number of source points."

OUT_DIR="out/gpu-memory-tests/"
OUT_CSV="out/gpu-memory-test.csv"

source ./options.sh # Include file.
mkdir -p ${OUT_DIR}

# List of point sources to try
POINTSOURCES=(100 200 300)

SLITHEIGHT=100 #15000 is realistic.

# Generate results
for (( i = 0; i < ${#POINTSOURCES[@]}; ++i )); do
    numpointsource=${POINTSOURCES[i]}

    OUT_FILENAME="${OUT_DIR}/${numpointsource}-point-source.txt"
    OUT_PROFILE_NAME="${OUT_DIR}/${numpointsource}-point-source.prof"

    if [[ ! -f ${OUT_DIR}/${numpointsource}-point-source.txt ]]; then
        echo "Have not run GPU memory test for ${numpointsource} point sources yet. Running..."

        ${CUDA_DIR}/nvprof --analysis-metrics --export-profile ${OUT_PROFILE_NAME} python -m optical_simulation.run_simulation --slitHeight ${SLITHEIGHT} --numOfPointSources ${numpointsource} > ${OUT_FILENAME} 2>&1
    else
        echo "Already run GPU memory test for ${numpointsource} point sources. Skipping. Delete file at ${OUT_FILENAME} to run again."
    fi

done

# From results, generate CSV file
echo "Generating CSV file at ${OUT_CSV}."
echo "There is no way that I can find to fill the memory transferred to CPU<->GPU by hand. That will have to be done
by opening the .prof files in the output directory."

# This does not overwrite your CSV in the case that you added stuff.
echo "sourcePoints,total-time (ms),mem-to-gpu-time (ms),kernel-time (ms),memory-transferred" >> ${OUT_CSV}

for f in ${OUT_DIR}/*-point-source.txt; do

    aline=""

    aline+=$(echo "${f}" | tr -dc '0-9')
    aline+=","

    aline+=$(cat ${f} | grep "total time:" | head -1 | tr -dc '0-9.')
    aline+=","

    aline+=$(cat ${f} | grep "mem-to-gpu time:" | head -1 | tr -dc '0-9.')
    aline+=","

    aline+=$(cat ${f} | grep "kernel time:" | head -1 | tr -dc '0-9.')
    aline+=","

    aline+="REPLACE ME; see the .prof files. I don't know how to extract how much memory is transferred via command line."

    echo ${aline} >> ${OUT_CSV}

done

cat ${OUT_CSV}
