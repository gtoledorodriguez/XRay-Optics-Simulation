#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 15 17:21:19 2017

"""
import argparse
import os  # Used in file saving function
from time import strftime
from typing import Tuple

import matplotlib.pyplot as plt
import numpy as np
from numba import cuda

from optical_simulation.cudaKernels import intensityCalculations
from optical_simulation.gratingLib.Grating import Grating
from optical_simulation.gratingLib.InitialSource import InitialSource

# Path to save images to.
current_path = os.path.abspath(os.path.dirname(__file__))
image_output_path = os.path.join(current_path, 'out')

if not os.path.exists(image_output_path):
    os.mkdir(image_output_path)

image_name = os.path.join(image_output_path, 'dottedProfile.png')


def get_args_from_command_line() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument('--screen_distance',
                        default=5e7,
                        type=int,
                        help='Not sure what this is exactly. Contact group or review code.')

    parser.add_argument('--screen_length',
                        default=1e7,
                        type=int,
                        help='Not sure what this is exactly. Contact group or review code.')

    parser.add_argument('--second_grating_distance',
                        default=5e7,
                        type=int,
                        help='Not sure what this is exactly. Contact group or review code.')

    parser.add_argument('--wavelength',
                        default=.56,
                        type=float,
                        help='The wavelength of the wave in nanometers.')

    parser.add_argument('--U_0',
                        default=1,
                        type=int,
                        help='The initial amplitude of the point source')

    parser.add_argument('--slitHeight',
                        default=10,
                        type=int,
                        help='Height of each slit in each grating (Used for 2D implementation)')

    parser.add_argument('--numOfSlits',
                        default=200,
                        type=int,
                        help='Number of slits in each grating')

    parser.add_argument('--numOfPointSources',
                        default=100,
                        type=int,
                        help='Number of point sources in eac slit')

    parser.add_argument('--numObsPoints',
                        default=1000,
                        type=int,
                        help='Number of observing points on the screen')

    parser.add_argument('--slitLength',
                        default=50,
                        type=int,
                        help='Length of the slits')

    parser.add_argument('--spacingType',
                        default='uniform',
                        type=str,
                        help='Geometry of the slits, Can be "uniform", "random", ...')

    parser.add_argument('--slit_Height',
                        default=5,
                        type=int,
                        help='Height of each slit in each grating (Used for 2D implementation)')

    parser.add_argument('--runNum',
                        default=1,
                        type=int,
                        help='Used to dynamically name files. Change every time you run a simulation. Otherwise it will write')

    # TODO: Fill in the rest of the arguments

    return parser.parse_args()


args = get_args_from_command_line()
screen_distance = args.screen_distance
screen_length = args.screen_length
second_grating_distance = args.second_grating_distance
wavelength = args.wavelength
slitHeight = args.slitHeight  #
numOfSlits = args.numOfSlits  # number of slits in each grating
numOfPointSources = args.numOfPointSources  # number of point sources in each slit
numObsPoints = args.numObsPoints  # number of observing points on the screen
slitLength = args.slitLength  # nm
slit_Height = args.slit_Height  # Height of each slit in each grating (Used for 2D implementation)
runNum = args.runNum  # Used to dynamically name files. Change every time you run a simulation. Otherwise it will write
spacingType = args.spacingType
U_0 = args.U_0

wavenumber = 2 * np.pi / wavelength
newSimulation = False
# over old data
############################################################################################################

print("Initializing vriables: Done")

# Observing screen size
# center of screen will automatically be at 0.5e7 nm
# Change this based on size of gratings
screenStart = 0e7
screenEnd = 1e7

timings = []

# create array of positions that represent an observing screen

print("Starting observation points")
timings.append(strftime("%Y/%m/%d %H:%M:%S"))
observingPositions = np.linspace(screenStart, screenEnd, numObsPoints)
print("Observation points made")

# Build gratings and fill with point sources

print("Starting first grating")
timings.append(strftime("%Y/%m/%d %H:%M:%S"))
firstGrating = Grating(x=0, length=screen_length, numberOfSlits=numOfSlits, slitWidth=slitLength,
                       slitHeight=slit_Height, sourcesPerSlit=numOfPointSources, sourceSpacing=spacingType)
print("First grating done")

# Build second grating and fill with point sources

print("Starting second grating")
timings.append(strftime("%Y/%m/%d %H:%M:%S"))
secondGrating = Grating(x=second_grating_distance, length=screen_length, numberOfSlits=numOfSlits, slitWidth=slitLength,
                        slitHeight=slit_Height, sourcesPerSlit=numOfPointSources, sourceSpacing=spacingType)
print("Second grating done")

# Define initial source
# Options are 'spherical' and 'plane'
# Initial source position is -(distance from first grating in nm)
timings.append(strftime("%Y/%m/%d %H:%M:%S"))
initSource = InitialSource(xPosition=-1e7, yPosition=screen_length / 2, waveType='plane', initialAmplitude=U_0)

# generate source amplitudes and phases based on the initial source and the first gratings point source positions
timings.append(strftime("%Y/%m/%d %H:%M:%S"))
sourceAmps, sourcePhase = initSource.propogate(firstGrating.x, firstGrating.pointSourcePositions, wavenumber,
                                               normalize=True)

# add these amplitudes to the first grating's point sources
timings.append(strftime("%Y/%m/%d %H:%M:%S"))
firstGrating.addAmplitudes(sourceAmps, sourcePhase)
# calculate information from firstGrating propagating to secondGrating
timings.append(strftime("%Y/%m/%d %H:%M:%S"))
intensities, amplitudes, phases = intensityCalculations(screen_distance, wavenumber, firstGrating.pointSourcePositions,
                                                        secondGrating.pointSourcePositions,
                                                        firstGrating.pointSourceAmplitudes,
                                                        firstGrating.pointSourcePhases)
# add necessary results to secondGrating's point sources
# print('Populating grating 2\n')
timings.append(strftime("%Y/%m/%d %H:%M:%S"))
secondGrating.addAmplitudes(amplitudes, phases)

# calculate information from secondGrating propagation to observingPositions
# print('Grating 2 to Screen:\n')
timings.append(strftime("%Y/%m/%d %H:%M:%S"))
intensities2, amplitudes2, phases2 = intensityCalculations(screen_distance, wavenumber,
                                                           secondGrating.pointSourcePositions, observingPositions,
                                                           secondGrating.pointSourceAmplitudes,
                                                           secondGrating.pointSourcePhases)
timings.append(strftime("%Y/%m/%d %H:%M:%S"))

if newSimulation:
    with open("onSecondGratingResults_%s_run00%s.txt" % (initSource.waveType, runNum), 'w') as f:
        f.write("#source wave type: %s, time taken: %s\n" % (initSource.waveType, tf1 - t01))
        f.write("#Intensity\tAmplitudes\t\tPhase\t\t\t\tPosition\n")
        for i, a, p, o in zip(intensities, amplitudes, phases, secondGrating.pointSourcePositions):
            f.write("%s\t%s\t%s\t%s\n" % (i, a, p, o))

    with open("onScreenResults_%s_run00%s.txt" % (initSource.waveType, runNum), 'w') as f:
        f.write("#source wave type: %s, time taken: %s" % (initSource.waveType, tf2 - t02))
        f.write("#Intensity\tAmplitudes\t\tPhase\t\t\t\tPosition\n")
        for i, a, p, o in zip(intensities2, amplitudes2, phases2, observingPositions):
            f.write("%s\t%s\t%s\t%s\n" % (i, a, p, o))

cuda.close()

print("Function, Timestamp")
print("observingPositions," + timings[0])
print("firstGrating," + timings[1])
print("secondGrating," + timings[2])
print("initSource," + timings[3])
print("initSource.propogate," + timings[4])
print("firstGrating.addAmplitudes," + timings[5])
print("calcIntensitiesCUDA," + timings[6])
print("secondGrating.addAmplitudes," + timings[7])
print("calcIntensitiesCUDA," + timings[8])
print("End of program," + timings[9] + "\n")

# quickly plot data to see if results are reasonable
plt.figure(figsize=(15, 8))
plt.plot(firstGrating.pointSourcePositions, firstGrating.pointSourceAmplitudes, '.r')
plt.savefig(image_name, transparent=True)
plt.xlabel('Position on First Grating (nm)', fontsize=25)
plt.ylabel('Amplitude', fontsize=25)
plt.title('Incident on First Grating', fontsize=30)
plt.show()

plt.figure(figsize=(15, 8))
plt.plot(secondGrating.pointSourcePositions, intensities, '.r')
plt.savefig(image_name, transparent=True)
plt.xlabel('Position on Second Grating (nm)', fontsize=25)
plt.ylabel('Normalized Intensity', fontsize=25)
plt.title('Incident on Second Grating', fontsize=30)
plt.show()

maxIntensities2 = max(intensities2)
intensities2 = [i / maxIntensities2 for i in intensities2]

obsPositionsMicrons = [i / 1000 for i in observingPositions]

plt.figure(figsize=(15, 8))
plt.plot(obsPositionsMicrons, intensities2, 'r')
plt.savefig(image_name, transparent=True)
plt.xlabel('Position on Observing Screen (nm)', fontsize=25)
plt.ylabel('Normalized Intensity', fontsize=25)
plt.title('Uniform Grating', fontsize=30)
plt.show()
