#!/usr/bin/env python
"""plots for light cones in """
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from particleBox import *
from monteCarloPathSampling import *


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
