#!/usr/bin/env bash

#python -m optical_simulation.2GratingDiffraction_final --imageSubdirs slitHeight1 --slitHeight=1
#python -m optical_simulation.2GratingDiffraction_final --imageSubdirs slitHeight2 --slitHeight=2
#python -m optical_simulation.2GratingDiffraction_final --imageSubdirs slitHeight3 --slitHeight=3


if ! [[ -d "./optical_simulation/image_output/pointSource_x_obsPoints" ]]; then

    # From 0 to 100 step 10 in point sources,
    for (( point_src=0; point_src<=100; point_src+=10)); do

        # From 0 to 1000 step 100 in observation points,
        for (( obs_point=0; obs_point<=1000; obs_point+=100 )); do

            # Run the simulation with two variables.
            python -m optical_simulation.2GratingDiffraction_final --imageSubdirs "pointSource_x_obsPoints" "pointSource${point_src}_x_obsPoint${obs_point}" \
                --numOfPointSources="${point_src}" --numObsPoints="${obs_point}"
        done
    done
fi

# If we haven't ran the 'numOfPointSourcesRuns' simulations, then run a LARGE amount of those simulations and create that directory.
if ! [[ -d "./optical_simulation/image_output/numOfPointSourcesRuns" ]]; then
    for (( n=0; n<=1000; n+=100)); do
        python -m optical_simulation.2GratingDiffraction_final --imageSubdirs "numOfPointSourcesRuns" "numOfPointSources${n}" --numOfPointSources="${n}"
    done
fi

# If we haven't ran the 'numObsPoints' simulations, then run a LARGE amount of those simulations and create that directory.
if ! [[ -d "./optical_simulation/image_output/numObsPointsRuns/" ]]; then
    for (( n=0; n<=1000; n+=50 )); do
        python -m optical_simulation.2GratingDiffraction_final --imageSubdirs "numObsPointsRuns" "numObsPoints${n}" --numObsPoints="${n}"
    done
fi

num=$(awk 'BEGIN{for(i=1; i<=2; i+=0.25)print i}')
if ! [[ -d "./optical_simulation/image_output/U_0/" ]]; then
    for n in $num; do
        python -m optical_simulation.2GratingDiffraction_final --imageSubdirs "U_0" "u_0${n}" --U_0="${n}"
    done
fi
