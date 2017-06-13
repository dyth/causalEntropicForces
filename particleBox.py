#!/usr/bin/env python
"""recreation of particle in a box example"""
import matplotlib.pyplot as plt

from monteCarloPathSampling import *


# state variables
stepSize = 5.0
depth = 20
start = [-50.0, 0.0]
bounds = ((-100.0, 100.0), (-100.0, 100.0))
dims = len(bounds)


def valid(walk, p):
    'determine whether a walk is valid'
    if ((p[0] < bounds[0][0]) or (p[0] > bounds[0][1]) or
        (p[1] < bounds[1][0]) or (p[1] > bounds[1][1])):
        return False
    else:
        return True


def reshape(walk):
    'change from list of coordinates to something usable in pyplot'
    unfurled = [[] for _ in range(dims)]
    [unfurled[i].append(w[i]) for i in range(dims) for w in walk]
    return unfurled

    
print "matplotlib finished building"
ax = plt.gca()
ax.set_title("Particle in a 2 dimensional box")
plt.ion()
plt.show()

ax2 = plt.gca()
ax2.set_title("Endpoint plots")

while True:
     walk = randomWalk([start], depth, dims, stepSize, valid)
     graphLists = reshape(walk)
     plt.figure(1)
     ax.plot(graphLists[0], graphLists[1])
     plt.figure(2)
     plt.plot(graphLists[0][-1], graphLists[1][-1], "o")
     plt.draw()
     plt.pause(0.01)
