#!/usr/bin/env python
"""particle in a box which drifts towards the centre"""
from numpy import array
from scipy.constants import Boltzmann
import matplotlib.pyplot as plt
import math

# state variables
length = 400.0
start = array([length/10.0, length/10.0])
bounds = ((0.0, length), (0.0, length/5.0))
dims = len(bounds)

KB = Boltzmann      # Boltzmann Constant
TAU = 10.0          # Time horizon
TR = 400000.0       # Temperature of heat reservoir of random movement
TC = 5.0 * TR       # Causal Path Temperature
TIMESTEP = 0.025    # Interval between random walk sampling
MASS = 10.0 ** -21

MEAN = 0.0
STDEV = math.sqrt((KB * TR * TIMESTEP**2.0) / (4.0 * MASS))
AMPLITUDE = math.sqrt(MASS * KB * TR) / TIMESTEP


def valid(walk, position):
    'determine whether a walk is valid'
    if ((position[0] < bounds[0][0]) or (position[0] > bounds[0][1]) or
        (position[1] < bounds[1][0]) or (position[1] > bounds[1][1])):
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
