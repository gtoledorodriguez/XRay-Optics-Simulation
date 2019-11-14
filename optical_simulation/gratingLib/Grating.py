from numpy import random

from optical_simulation.gratingLib.PointSource import PointSource
from optical_simulation.gratingLib.Slit import Slit


class Grating:

    def __init__(self, x, length, numberOfSlits, slitWidth, slitHeight, sourcesPerSlit, sourceSpacing):

        # all attributes are necessary for a grating to initialize itself and fill itself with slits and point sources
        self.x = x
        self.length = length
        self.numberOfSlits = numberOfSlits
        self.slitWidth = slitWidth
        self.slitHeight = slitHeight
        self.sourceSpacing = sourceSpacing
        self.sourcesPerSlit = sourcesPerSlit
        self.slits = []
        self.pointSourcePositions = []
        self.pointSourceAmplitudes = []
        self.pointSourcePhases = []

        # fill grating with slits, makeSlits also fills slits with point sources
        makeSlits(self, self.slitWidth, self.slitHeight, self.sourcesPerSlit, self.sourceSpacing)

    def addAmplitudes(self, newAmplitudes, newPhases):

        # method takes an array of amplitudes, replaces point source amplitude array, and populates all slits and
        # point sources with new amplitudes

        self.pointSourceAmplitudes = newAmplitudes
        self.pointSourcePhases = newPhases
        '''
        for slit in self.slits:
            for i in range(0, len(slit) - 1):
                for source, newAmplitude in zip(slit[i].sources, newAmplitudes):
                    source.amplitude = newAmplitude
        '''


def makeSlits(grating, slit_width, slit_height, sourcesPerSlit, source_spacing):
    # This function will create a set amount of slits based on the amount of slits a Grating class wants. Each slit is created with
    # 'num_sources' number of sources with a slit width of 'slit_width.' Depending on the amount of sources a grating wants, this
    # function sets up different diffraction scenarios, like single slit diffraction, double slit diffraction, and Grating
    # diffraction

    if grating.numberOfSlits > 2:
        # Modeling a Grating with numberOfSlits
        # this Grating is expected to have at least a slit_width of distance between each slit
        # numberOfSlits is a variable input and each should start from the center and built outwards

        if grating.numberOfSlits % 2 == 0:

            center = grating.length / 2

            i = 0

            while grating.numberOfSlits / 2 > i:
                slit1_y = center + slit_width * 0.5 + 2 * i * slit_width
                slit2_y = center - slit_width * 1.5 - 2 * i * slit_width

                # Made slit 2 dimentional by making an array of slit height size, with identical slits.
                slit_1 = [slit1_y] *slit_height
                slit_2 = [slit2_y] *slit_height
                
                grating.slits.append(slit_1)
                grating.slits.append(slit_2)

                i += 1
            for slit in grating.slits:
                for x in range(0, slit_height - 1):
                    y_position = float(slit_width / float(sourcesPerSlit - 1))
                    grating.pointSourcePositions.append(slit[x])

                    for i in range(0, sourcesPerSlit - 2):
                        grating.pointSourcePositions.append(slit[x]+y_position)
                        y_position += y_position

                    grating.pointSourcePositions.append(slit[x]+slit_width)
                    fh = open('pspos.txt', 'w')
                    for pos in grating.pointSourcePositions:
                        fh.write(str(pos)+'\n')
                    fh.close()