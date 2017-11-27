#!/usr/bin/env python
"""particle in a box which drifts towards the centre"""
from numpy import array
from scipy.constants import Boltzmann
from scipy.stats import norm
from math import sqrt, log

class ParticleBox:

    def __init__(self):
        # state variables
        self.length = 400.0
        self.start = array([self.length/10.0, self.length/10.0])
        self.bounds = ((0.0, self.length), (0.0, self.length/5.0))
        self.DIMS = len(self.bounds)

        self.KB = Boltzmann      # Boltzmann Constant
        self.TAU = 10.0          # Time horizon
        self.TR = 400000.0       # Temperature of random movement
        self.TC = 5.0 * self.TR  # Causal Path Temperature
        self.TIMESTEP = 0.025    # Interval between random walk sampling
        self.MASS = 10.0 ** -21

        self.MEAN = 0.0
        self.AMPLITUDE = sqrt(self.MASS * self.KB * self.TR) / self.TIMESTEP
        self.DISTRIBUTION = norm(0.0, 1.0)


    def valid(self, walk, position):
        'determine whether a walk is valid'
        if ((position[0] < self.bounds[0][0]) or
            (position[0] > self.bounds[0][1]) or
            (position[1] < self.bounds[1][0]) or
            (position[1] > self.bounds[1][1])):
            return False
        else:
            return True
