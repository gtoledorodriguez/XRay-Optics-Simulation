#!/usr/bin/env bash

#python -m optical_simulation.2GratingDiffraction_final --imageSubdir=slitHeight1 --slitHeight=
#python -m optical_simulation.2GratingDiffraction_final --imageSubdir=slitHeight2 --slitHeight=2
#python -m optical_simulation.2GratingDiffraction_final --imageSubdir=slitHeight3 --slitHeight=3


for (( n=0; n<=1000; n+=250 )); do
    echo "$n"

    python -m optical_simulation.2GratingDiffraction_final --imageSubdir="numObsPoints${n}" --numObsPoints="${n}"
    ls $n

done

