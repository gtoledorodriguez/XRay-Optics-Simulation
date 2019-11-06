#!/usr/bin/env bash

echo "This file runs a series of tests that vary the amount of source points per slit to see how runtime and memory \
usage will vary when increasing the number of source points."

OUT_DIR="out/gpu-memory-tests/"
OUT_CSV="out/gpu-memory-test.csv"

source ./options.sh # Include file.
mkdir -p ${OUT_DIR}

# List of point sources to try
POINTSOURCES=(100 200 300)

SLITHEIGHT=50 #15000 is realistic.

OBSPOINTS=150

## DEBUG PARAMS: These are fast but not realistic!
#POINTSOURCES=(5 10 20 30 40 50 60 70 80 90 100 200 300 400)
#SLITHEIGHT=5
#OBSPOINTS=30


# Vary point sources
for (( i = 0; i < ${#POINTSOURCES[@]}; ++i )); do

    # One of n point sources
    numpointsource=${POINTSOURCES[i]}

    # Place to redirect stdout of the nvprof command
    OUT_FILENAME="${OUT_DIR}/${numpointsource}-point-source.txt"
    OUT_PROFILE_NAME="${OUT_DIR}/${numpointsource}-point-source.prof"

    # If stdout file from nvprof command does not exist,
    if [[ ! -f ${OUT_DIR}/${numpointsource}-point-source.txt ]]; then
        echo "Have not run GPU memory test for ${numpointsource} point sources yet. Running..."

        # Run the profiling command.
        ${NVPROF_BIN} --print-gpu-trace --export-profile ${OUT_PROFILE_NAME} \
            python -m optical_simulation.run_simulation --slitHeight ${SLITHEIGHT} --numOfPointSources ${numpointsource} \
            --numObsPoints $OBSPOINTS > ${OUT_FILENAME} 2>&1
    else
        echo "Already run GPU memory test for ${numpointsource} point sources. Skipping. Delete file at ${OUT_FILENAME} to run again."
    fi

done

# From results, generate CSV file
echo "Generating CSV file at ${OUT_CSV}."
echo "There is no way that I can find to fill the memory transferred to CPU<->GPU by hand. That will have to be done
by opening the .prof files in the output directory."

# This does not overwrite your CSV in the case that you added stuff.
echo "sourcePoints,total-time (ms),mem-to-gpu-time (ms),kernel-time (ms),slit-height,obs-points,bytes-transferred-total-DtoH,bytes-transferred-total-HtoD" > ${OUT_CSV}

for f in ${OUT_DIR}/*-point-source.txt; do

    aline=""

    # The source points from the filename.
    # TODO: This is poor form to encode the source points here.
    # TODO: Ideally, we should be able to run over a matrix of varying parameters and see how they all affect runtime.
    # TODO: This information should be encoded elsewhere.
    aline+=$(echo "${f}" | tr -dc '0-9')
    aline+=","

    # total time it took to run the sim
    aline+=$(cat ${f} | grep "total time:" | head -1 | tr -dc '0-9.')
    aline+=","

    # Time to transfer data from memory to GPU
    aline+=$(cat ${f} | grep "mem-to-gpu time:" | head -1 | tr -dc '0-9.')
    aline+=","

    # Time to run gpu sims
    aline+=$(cat ${f} | grep "kernel time:" | head -1 | tr -dc '0-9.')
    aline+=","

    # Height of slit. Currently static.
    aline+=${SLITHEIGHT}
    aline+=","

    # Observation points. Currently static.
    aline+=${OBSPOINTS}
    aline+=","

    # GPU->CPU memory transfer total in bytes
    echo "GPU to CPU mem transfer: (d to h)" # gpu to cpu
    aline+=$(cat ${f} | grep "DtoH" | awk '{print $8}' | python3 scripts/byte_adder.py)
    aline+=","

    # CPU->GPU memory transfer total in bytes
    echo "CPU to GPU mem transfer: (h to d)" # cpu to gpu
    aline+=$(cat ${f} | grep "HtoD" | awk '{print $8}' | python3 scripts/byte_adder.py)
#    aline+=","

    echo ${aline} >> ${OUT_CSV}

done

cat ${OUT_CSV}
