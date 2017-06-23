#!/usr/bin/env python
"""as accurate an implementation as possible"""
import math, sys, os
import matplotlib.pyplot as plt
import numpy as np

from monteCarloGaussianPaths import *

sys.path.append(os.path.join(os.path.dirname(sys.path[0]), 'particleBox'))
from particleBox import *


# global entropic variables
samples, steps = 400, 10
depth = tau / timeStep
variance = (kb * Tr * timeStep**2.0) / (4.0 * mass) # variance per step


def totalVolume(logProbs):
    largest = max(logProbs)
    others = sum([math.exp(i - largest) for i in logProbs])
    others = math.log(1.0 + others)
    return largest - others


def entropicForce(pos):
    'calculate where the next step should be with mean of all samples'
    # sample and return first points and the log-likelihoods
    stdev = math.sqrt(variance)
    config = configuration(dims, stdev, valid, mass)
    points, logProbs = monteCarloGaussianPaths(pos, samples, config, depth)
    # calculate mean of first step and the volume of the log-likelihoods
    mean = np.mean(points, axis=0)
    volume = [totalVolume(logProbs[i]) for i in range(dims)]
    # calculate the total entropic force
    total = [0.0 for _ in range(dims)]
    for j in range(samples):
        difference = points[j] - mean
        for i in range(dims):
            total[i] += difference[i] * (volume[i] - logProbs[i][j])
    return 4.0 * Tc * np.array(total) / (float(samples**2) * Tr * timeStep)


def forcing(pos, steps, path):
    'return path taken by forcing of particle, similar to the randomWalk'
    if steps == 0:
        return path
    else:
        newPos = pos + entropicForce(pos)
        if valid(path, newPos):
            path.append(newPos.tolist())
            steps -= 1
            print "moved", j, "steps, now at", newPos
    return forcing(newPos, steps, path)



print "starting position", start
path = [start.toList()] + forcing(start, steps, [])
path = [[p[i] for p in path] for i in range(dims)]

plt.figure()
ax = plt.gca(aspect = 'equal')
ax.set_title("Particle in a 2 dimensional box")
ax.set_xlim(bounds[0][0], bounds[0][1])
ax.set_ylim(bounds[1][0], bounds[1][1])
ax.plot(path[0], path[1], linewidth=0.25, color='k')
plt.show()
