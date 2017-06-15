#!/usr/bin/env python
"""recreation of particle in a box example"""
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from numpy import array

from monteCarloPathSampling import *
from kde import *

# state variables
stepSize = 5.0
depth = 20
start = [-50.0, 0.0]
bounds = ((-100.0, 200.0), (-100.0, 100.0))
dims = len(bounds)


def valid(walk, p):
    'determine whether a walk is valid'
    if ((p[0] < bounds[0][0]) or (p[0] > bounds[0][1]) or
        (p[1] < bounds[1][0]) or (p[1] > bounds[1][1])):
        return False
    else:
        return True


def reshape(walk):
    'change from list of coordinates to list of ith coordinate'
    unfurled = [[] for _ in range(dims)]
    [unfurled[i].append(w[i]) for i in range(dims) for w in walk]
    return unfurled



print "matplotlib finished building"
"""
plt.figure(1)
ax = plt.gca(aspect = 'equal')
ax.set_title("Particle in a 2 dimensional box")
ax.set_xlim(bounds[0][0], bounds[0][1])
ax.set_ylim(bounds[1][0], bounds[1][1])

plt.figure(2)
ax2 = plt.gca(aspect = 'equal')
ax2.set_title("Endpoint plots")
ax2.set_xlim(bounds[0][0], bounds[0][1])
ax2.set_ylim(bounds[1][0], bounds[1][1])

fig = plt.figure(3)
ax3 = fig.add_subplot(111, projection='3d', aspect = 'equal')
ax3.set_title("Light Cone")
ax3.set_xlim(bounds[0][0], bounds[0][1])
ax3.set_ylim(bounds[1][0], bounds[1][1])
ax3.set_zlim(0, depth)

plt.ion()
plt.show()

while True:
     walk = randomWalk([start], depth, dims, stepSize, valid)
     graphLists = reshape(walk)
     
     plt.figure(1)
     ax.plot(graphLists[0], graphLists[1])
     
     plt.figure(2)
     plt.plot(graphLists[0][-1], graphLists[1][-1], "o")
     
     plt.figure(3)
     ax3.plot(graphLists[0], graphLists[1], range(len(graphLists[0])))
  
     plt.draw()
     plt.pause(0.01)
"""

X = monteCarloPathSampling(start, 100, depth, dims, stepSize, valid)
print "Finished Monte Carlo Path Sampling"

plt.figure()
ax = plt.gca(aspect = 'equal')
ax.set_title("KDE and points")
ax.set_xlim(bounds[0][0], bounds[0][1])
ax.set_ylim(bounds[1][0], bounds[1][1])
# strangely, after KDE, the axes have swapped, so plot points swapped round
[plt.plot(i[1], i[0], "o") for i in X]

X = array(X)

xmin, xmax, ymin, ymax = bounds[0][0], bounds[0][1], bounds[1][0], bounds[1][1]
Nx, Ny = xmax - xmin, ymax - ymin

dens1 = estimate(X, xmin, xmax, ymin, ymax, Nx, Ny)
plot(dens1, xmin, xmax, ymin, ymax)
