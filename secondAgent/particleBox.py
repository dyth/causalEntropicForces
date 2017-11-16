#!/usr/bin/env python
"""particle in a box which drifts towards the centre"""
from numpy import array
from scipy.constants import Boltzmann
from scipy.stats import norm
import matplotlib.pyplot as plt
import math

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
        self.AMPLITUDE = math.sqrt(self.MASS*self.KB*self.TR) / self.TIMESTEP
        self.DISTRIBUTION = norm(self.MEAN, self.AMPLITUDE)


    def valid(self, walk, position):
        'determine whether a walk is valid'
        if ((position[0] < self.bounds[0][0]) or
            (position[0] > self.bounds[0][1]) or
            (position[1] < self.bounds[1][0]) or
            (position[1] > self.bounds[1][1])):
            return False
        else:
            return True


def plot(path):
    'plot the path of the particle on a pyplot graph'
    plt.figure()
    ax = plt.gca(aspect = 'equal')
    ax.set_title("Particle in a 2 dimensional box")
    ax.set_xlim(bounds[0][0], bounds[0][1])
    ax.set_ylim(bounds[1][0], bounds[1][1])
    path = [[p[i] for p in path] for i in range(dims)]
    ax.plot(path[0], path[1], linewidth=0.25, color='k')
    plt.show()
