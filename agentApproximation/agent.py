#!/usr/bin/env python
"""perform causal entropic forces on context"""
import math, sys, os
import matplotlib.pyplot as plt

from monteCarloPathSampling import *
from kde import *

sys.path.append(os.path.join(os.path.dirname(sys.path[0]), 'particleBox'))
from particleBox import *


# state variables
stepSize, depth, samples, steps = 5.0, 20, 50, 1
    

def force(pos, bounds, number, stepSize):
    'calculate where the next step should be'
    points = monteCarloPathSampling(pos, samples, depth, dims, stepSize, valid)
    logProb, coords = estimate(points, bounds, number)
    move = average(logProb, coords, pos)
    magnitude = math.sqrt(sum([m**2.0 for m in move]))
    return [-stepSize * m / magnitude for m in move]


def forcing(position, bounds, steps, stepSize, dims):
    'return path taken by forcing of particle'
    number = [b[1] - b[0] for b in bounds]
    path = []
    for j in range(steps):
        move = force(position, bounds, number, stepSize)
        position = [position[i] + move[i] for i in range(dims)]
        path.append(position)
        print "moved", move, j, "steps, now at", position
    return path



path = forcing(start, bounds, steps, stepSize, dims)
path = [[p[i] for p in path] for i in range(dims)]

plt.figure()
ax = plt.gca(aspect = 'equal')
ax.set_title("Particle in a 2 dimensional box")
ax.set_xlim(bounds[0][0], bounds[0][1])
ax.set_ylim(bounds[1][0], bounds[1][1])
ax.plot(path[0], path[1], linewidth=0.1, color='k')
plt.show()
