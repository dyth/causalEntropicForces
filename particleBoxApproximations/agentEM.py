#!/usr/bin/env python
"""perform causal entropic forces on context using expectation maximisation"""
import math
import matplotlib.pyplot as plt

from particleBox import *
from monteCarloPathSampling import *
from kdeEM import *


# state variables
stepSize, depth, samples, steps = 5.0, 400, 400, 100


def force(pos, bounds, number, stepSize):
    'calculate where the next step should be'
    points = monteCarloPathSampling(pos, samples, depth, dims, stepSize, valid)
        
    limit = []
    for i in range(dims):
        partialList = [p[i] for p in points]
        limit.append([min(partialList), max(partialList)])
    number = [b[1] - b[0] for b in limit]

    
    logProb, coords = estimate(points, limit, number)
    return average(logProb, coords)


def forcing(position, bounds, steps, stepSize, dims):
    'return path taken by forcing of particle'
    number = [b[1] - b[0] for b in bounds]
    path = []
    for j in range(steps):
        position = force(position, bounds, number, stepSize)
        path.append(position)
        print "moved", j, "steps, now at", position
    return path



path = forcing(start, bounds, steps, stepSize, dims)
path = [[p[i] for p in path] for i in range(dims)]

plt.figure()
ax = plt.gca(aspect = 'equal')
ax.set_title("Particle in a 2 dimensional box")
ax.set_xlim(bounds[0][0], bounds[0][1])
ax.set_ylim(bounds[1][0], bounds[1][1])
ax.plot(path[0], path[1], linewidth=0.25, color='k')
plt.show()
