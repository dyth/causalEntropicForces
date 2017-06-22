#!/usr/bin/env python
"""particle in a box which drifts towards the centre"""
from numpy import array
from scipy.constants import Boltzmann

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
