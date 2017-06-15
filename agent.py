#!/usr/bin/env python
"""perform kernel density estimation on 2D grid"""
import math
from numpy import array
from particleBox import *
from monteCarloPathSampling import *
from kde import *

# state variables
stepSize, depth = 5.0, 100

def average(logProb, points, position):
    'take weighted average of logProb and points offset to find mean outcome'
    mean = array([0.0, 0.0])
    points = array([point - position for point in points])
    for index in range(len(points)):
        mean += logProb[index] * points[index]
    return [m / float(len(points)) for m in mean]
    

def force(position, bounds, number, stepSize):
    'calculate where the next step should be'
    points = monteCarloPathSampling(start, 100, depth, dims, stepSize, valid)
    logProb, allPoints = estimate(points, bounds, number)
    move = average(logProb, allPoints, position)
    magnitude = math.sqrt(sum([m**2.0 for m in move]))
    return [-stepSize * m / magnitude for m in move]


def forcing(position, bounds, steps, stepSize, dims):
    'return path taken by forcing of particle'
    number = [b[1] - b[0] for b in bounds]
    path = []
    for j in range(steps):
        move = force(position, bounds, number, stepSize)
        position = [int(position[i] + move[i]) for i in range(dims)]
        path.append(position)
        print "moved", move, j, "steps, now at", position
    return path



path = forcing(start, bounds, 100, stepSize, dims)
blank = [[] for _ in range(dims)]
graphLists = [blank[i].append(p[i]) for i in range(dims) for p in path]

plt.figure()
ax = plt.gca(aspect = 'equal')
ax.set_title("Particle in a 2 dimensional box")
ax.set_xlim(bounds[0][0], bounds[0][1])
ax.set_ylim(bounds[1][0], bounds[1][1])
ax.plot(graphLists[0], graphLists[1], linewidth=0.1, color='k')
plt.show()
