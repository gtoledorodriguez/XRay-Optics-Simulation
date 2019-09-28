#!/usr/bin/env bash

#python -m optical_simulation.2GratingDiffraction_final --imageSubdir=slitHeight1 --slitHeight=
#python -m optical_simulation.2GratingDiffraction_final --imageSubdir=slitHeight2 --slitHeight=2
#python -m optical_simulation.2GratingDiffraction_final --imageSubdir=slitHeight3 --slitHeight=3


for (( n=0; n<=1000; n+=250 )); do
    echo "$n"

    python -m optical_simulation.2GratingDiffraction_final --imageSubdir="numObsPoints${n}" --numObsPoints="${n}"
    ls $n

done


# If we haven't ran the 'numObsPoints' simulations, then run a LARGE amount of those simulations and create that directory.
if ! [[ -d "./image_output/numObsPointsRuns/" ]]; then
    for (( n=0; n<=1000; n+=50 )); do
        python -m optical_simulation.2GratingDiffraction_final --imageSubdirs "numObsPointsRuns" "numObsPoints${n}" --numObsPoints="${n}"
    done
fi
