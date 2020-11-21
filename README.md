# X-Ray Optics Simulation

## Introduction
This is the official repository for IPRO 497 - Antimatter Interferometer ***as of Fall 2020***. All code needed to run the Optival Simulation can be found here. Any students in this course should first fork the repository and update any time specific information pertaining to when they took the course. For more information on contributing, visit the contributing section of this document. For any other information regarding the course, please contact Dr. Daniel Kaplan or Dr. Derrick Mancini.

The purpose of this IPRO is to experimentally answer if matter and antimatter repel each other throguh gravity. The methodwe use to answer this is to measure the effects of gravity on antimatter using muonium and seeing if antmatter responds to gravity in a measurable manner. The equipment to undergo this expirement is expensive and time consuming to make. A simulation of this experiment would prove useful because it is significantly easier to test prototypes or other changes without having to spend time or money on hardware that may or may not work.

## Dependencies

### Hardware/OS

You will need a computer with an NVIDIA GPU that supports CUDA.You will also need to use Linux. WSL may work. Virtualization will likely not work unless it offers GPU passthrough. We used a system with the following configuration:

#### CPU
(2) Intel(R) Xeon(R) CPU E5-2630 v2 @ 2.60GHz

#### Memory
(5) Micron 4GB MT9JSF51272PZ-1G9E2

#### GPU
(1) TITAN Xp
(1) Tesla K40c

#### Software

Install [Conda](https://docs.conda.io/en/latest/) with Python 3.6 or greater.
Install the [NVIDIA CUDA Toolkit](https://docs.nvidia.com/cuda/cuda-installation-guide-linux/index.html).
Once installed, you should edit `/options.sh` to update the path of the CUDA binary folder. By default, we use `/usr/local/cuda-9.1/bin/` because we have multiple versions and want to use that specific version of NVIDIA CUDA.

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

## Notes on 3d_plots folder
One of the tasks from Fall 2020 was to make the whole simulation 3-dimensional. Unfortunetly, there was not enough time left in the semester to finish. This task is a long-term goal and other groups should continue where we left off if they are willing to make it the theme for their entire semester. There can be many benefits to completing this task such as incorporating strut changes and more up to date computing hardware.

## Contrbuting
Previously to Fall 2020, there was no default way to keep track of semester progress that we were aware of beside GitHub. To reduce confusion and ease the transition process between semester groups, please follow this section to make the appropriate changes that will signify which repo is the current version and to let future students know what each section of code does. This is crucial since a lot of time can be wasted trying to figure out what other people did. 

1. Fork the previous semester's repository.
2. Update the Introduction section of the README.md file to reflect your current semester. Specifically, change the semester description ***in bold***.
3. Add as much documentation as possible to your semester's Google Drive folder. Write everything clearly as if a complete stranger will need to read it one day.
4. COMMENT YOUR CODE.



## Resources
The Background folder in Google Drive
[Measuring Antimatter Gracity with Muonium](https://www.epj-conferences.org/articles/epjconf/pdf/2015/14/epjconf_icnfp2014_05008.pdf)
[What is an Interferometer?](https://www.ligo.caltech.edu/page/what-is-interferometer)
[Muonium Wikipedia Article](https://en.wikipedia.org/wiki/Muonium)
[Anaconda Cheat Sheet](https://docs.conda.io/projects/conda/en/4.6.0/_downloads/52a95608c49671267e40c689e0bc00ca/conda-cheatsheet.pdf)
[CUDA Documentation](https://docs.nvidia.com/cuda/)
