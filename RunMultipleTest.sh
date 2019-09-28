#!/usr/bin/env bash

#python -m optical_simulation.2GratingDiffraction_final --imageSubdirs slitHeight1 --slitHeight=1
#python -m optical_simulation.2GratingDiffraction_final --imageSubdirs slitHeight2 --slitHeight=2
#python -m optical_simulation.2GratingDiffraction_final --imageSubdirs slitHeight3 --slitHeight=3


# If we haven't ran the 'numOfPointSourcesRuns' simulations, then run a LARGE amount of those simulations and create that directory.
if ! [[ -d "./optical_simulation/image_output/numOfPointSourcesRuns" ]]; then
    for (( n=0; n<=100; n+=10)); do
        python -m optical_simulation.2GratingDiffraction_final --imageSubdirs "numOfPointSourcesRuns" "numOfPointSources${n}" --numOfPointSources="${n}"
    done
fi

# If we haven't ran the 'numObsPoints' simulations, then run a LARGE amount of those simulations and create that directory.
if ! [[ -d "./optical_simulation/image_output/numObsPointsRuns/" ]]; then
    for (( n=0; n<=1000; n+=50 )); do
        python -m optical_simulation.2GratingDiffraction_final --imageSubdirs "numObsPointsRuns" "numObsPoints${n}" --numObsPoints="${n}"
    done
fi
