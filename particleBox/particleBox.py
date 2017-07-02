#!/usr/bin/env python
"""particle in a box which drifts towards the centre"""
from numpy import array
from scipy.constants import Boltzmann
import matplotlib.pyplot as plt

# state variables
length = 400.0
start = array([length/10.0, length/10.0])
bounds = ((0.0, length), (0.0, length/5.0))
dims = len(bounds)

kb = Boltzmann      # Boltzmann Constant
tau = 10.0          # Time horizon
Tr = 400000.0       # Temperature of heat reservoir of random movement
Tc = 5.0 * Tr       # Causal Path Temperature
timeStep = 0.025    # Interval between random walk sampling
mass = 10.0 ** -21


def valid(walk, p):
    'determine whether a walk is valid'
    if ((p[0] < bounds[0][0]) or (p[0] > bounds[0][1]) or
        (p[1] < bounds[1][0]) or (p[1] > bounds[1][1])):
        return False
    else:
        return True

        
def randomStep(dist, pos):
    'generate piecewise continuous Gaussian step and its likelihood'
    # this is a simulation of a Wiener Process, by the normal distribution
    point = dist.rvs(size=dims)
    return pos + point, dist.logpdf(point)


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
