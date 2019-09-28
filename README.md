# X-Ray Optics Simulation

## Running this code

Install Conda with Python 3.6.

Run `conda deactivate` to deactivate the `base` environment.

Run `conda env create -f environment.yml` in this directory to create a Conda environment with all dependencies specified in `environment.yml`.

The environment is called `agis`.

Run `conda activate agis` to use the virtual environment configured with Conda for this project.

Then run `python -m optical_simulation.2GratingDiffraction_final` to run the slit simulation.

You can also run `python -m optical_simulation.demo.runMultiCoreTest` to run the multi-core test.

There is a shell script called `RunMultipleTest.sh` that will run multiple simulations with slightly different parameters.

## Installing new packages

Add the package to `environment.yml`.

Run `conda env update -f environment.yml` in this directory to update Conda's environment from this file.
