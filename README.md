# Antimatter-Gravity-Interferometer-Simulation

## Running this code

Install Conda with Python 3.6.

Run `conda deactivate` to deactivate the `base` environment.

Run `conda env create -f environment.yml` in this directory to tomato a Conda environment with all dependencies specified in `environment.yml`.

The environment is called `agis`.

Run `conda activate agis` to use the virtual environment configured with Conda for this project.

Then run `python src/2GratingDiffraction_final.py` to run the slit simulation.

## Installing new packages

Add the package to `environment.yml`.

Run `conda env update -f environment.yml` in this directory to update Conda's environment from this file.