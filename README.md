# X-Ray Optics Simulation

## Dependencies

You will need a computer with an NVIDIA GPU that supports CUDA.

You will also need to use Linux. WSL may work. Virtualization will likely not work unless it offers GPU passthrough

Install [Conda](https://docs.conda.io/en/latest/) with Python 3.6 or greater.

Install the [NVIDIA CUDA Toolkit](https://docs.nvidia.com/cuda/cuda-installation-guide-linux/index.html).

## Running this code

Run `conda deactivate` to deactivate the `base` environment.

Run `conda env create -f environment.yml` in this directory to create a Conda environment with all dependencies specified in `environment.yml`.

The environment is called `agis`.

Run `conda activate agis` to use the virtual environment configured with Conda for this project.

Run `bash scripts/install_extra_conda_dependencies.sh` to install dependencies we cannot specify in the `environment.yml` file.

Then run `python -m optical_simulation.run_simulation` to run the slit simulation.

You can also run `python -m optical_simulation.demo.runMultiCoreTest` to run the multi-core test.

There is a shell script called `RunMultipleTests.sh` that will run multiple simulations with slightly different parameters.

There are also profiling scripts called `profile-*.sh`.

## Installing new packages

Add the package to `environment.yml`.

Run `conda env update -f environment.yml` in this directory to update Conda's environment from this file.
