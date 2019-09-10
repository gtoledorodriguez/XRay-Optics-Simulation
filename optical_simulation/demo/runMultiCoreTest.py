import sys

from optical_simulation.demo import multiCoreTest

import matplotlib.pyplot as plt
import argparse

TESTING = False
"""Are we testing this program w/o command line input?"""


def get_args_from_command_line():
    """Get arguments from the command line."""
    # TODO: When running this program from the command line, no description is given for what arguments
    # this program should accept. We should use `argparse` to parse command-line args.

    parser = argparse.ArgumentParser()
    parser.add_argument('--runs',
                        required=True,
                        type=int,
                        help="Number of times program is to run, with linearly increasing processes")
    parser.add_argument('--cores',
                        required=True,
                        type=int,
                        help="Number of cores to utilize with multiprocessor")
    parser.add_argument('--multiplier',
                        required=True,
                        type=int,
                        help="Number of processes to increase by in each iteration of for loop")
    parser.add_argument('--time',
                        required=True,
                        type=float,
                        help="Sleep timer to mitigate our code's race condition")
    # TODO: Parse the rest of the command-line arguments using this parser object!

    # Parse args from command line
    args = parser.parse_args()

    # Args for program
    runs = args.runs
    cores = args.cores
    multiplier = args.multiplier
    time = args.time

    # TODO: Don't use sys.argv for the rest of the arguments!

    return runs, cores, multiplier, time


if __name__ == '__main__':

    if TESTING:
        runs = 5
        cores = 8
        multiplier = 200000
        time = 1
    else:
        runs, cores, multiplier, time = get_args_from_command_line()

    # Arrays used for storing results
    timesArray = []
    ratioArray = []

    xLabel = 'Processes running *(' + str(multiplier) + ")"
    # Run demo n times, increasing number of processes to run each time by [multiplier], split between [cores] cores
    # append results to arrays
    for x in range(1, runs):
        print("{}th run".format(x))

        multi, single = multiCoreTest.run_multicore_test(cores, x * multiplier, time)
        timesArray.append((multi, single))
        ratioArray.append((((multi / single) * 100) - 100) * -1)

    # Plot the results: First subplot shows comparison in run time, second subplot shows the reduction (Or increase) in time to run-
    # - on multiple cores
    plt.subplot(2, 1, 1)
    plt.title(str(cores) + " cores (blue) vs Single core (Orange)")
    plt.ylabel('Time to run (s)')
    plt.plot(timesArray)

    plt.subplot(2, 1, 2)
    plt.xlabel(xLabel)
    plt.ylabel("Reduction in time (%)")
    plt.plot(ratioArray)
    plt.show()
