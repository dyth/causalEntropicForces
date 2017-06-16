#!/usr/bin/env python
"""Unravelling of functions in agent.py applied to particleBox for plotting"""
import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from numpy import array

from particleBox import *
from monteCarloPathSampling import *
from kde import *


# state variables and basic setup of the graphs
stepSize, depth, samples, steps = 5.0, 100, 100, 2
im = False # make True if you want to save images

plt.ion()
plt.show()


def force(pos, bounds, number, stepSize, ax, ax2, ax3):
    'calculate where the next step should be'
    points = []
    for _ in range(samples):
        # do random walks and append to lists for plotting
        walk = randomWalk([pos], depth, dims, stepSize, valid)
        points.append(walk[-1])
        walk = [[w[i] for w in walk] for i in range(dims)]
        # plot lines and points on graph
        plt.figure(1)
        ax.plot(walk[0], walk[1])
        plt.figure(2)
        plt.plot(walk[0][-1], walk[1][-1], "o")
        plt.figure(3)
        ax3.plot(walk[0], walk[1], range(len(walk[0])))
        plt.draw()
        plt.pause(0.005)

    if im:
        plt.figure(2)
        plt.savefig('images/2DPoints.png', dpi=900)
        
    # calculate the next step
    logProb, coords = estimate(points, bounds, number)
    move = average(logProb, coords, pos)
    magnitude = math.sqrt(sum([m**2.0 for m in move]))
    move = [-stepSize * m / magnitude for m in move]
    # plot kernel density estimation on graph with points
    logProb = array(logProb).reshape(tuple(reversed(number)))
    plt.figure(2)
    extent = (bounds[0][0], bounds[0][1], bounds[1][0], bounds[1][1])
    ax2.imshow(logProb, origin='lower', extent=extent, cmap=plt.cm.binary)
    plt.draw()
    return move


def forcing(position, bounds, steps, stepSize, dims):
    'return path taken by forcing of particle'
    number = [b[1] - b[0] for b in bounds]
    path = []
    for j in range(steps):
        plt.figure(1)
        plt.clf()
        ax = plt.gca(aspect = 'equal')
        ax.set_title("Particle in a 2 dimensional box")
        ax.set_xlim(bounds[0][0], bounds[0][1])
        ax.set_ylim(bounds[1][0], bounds[1][1])

        plt.figure(2)
        plt.clf()
        ax2 = plt.gca(aspect = 'equal')
        ax2.set_title("Endpoint plots")
        ax2.set_xlim(bounds[0][0], bounds[0][1])
        ax2.set_ylim(bounds[1][0], bounds[1][1])

        fig = plt.figure(3)
        plt.clf()
        ax3 = fig.add_subplot(111, projection='3d', aspect = 'equal')
        ax3.set_title("Light Cone")
        #ax3.set_zlim(0, depth)

        move = force(position, bounds, number, stepSize, ax, ax2, ax3)
        position = [position[i] + move[i] for i in range(dims)]
        path.append(position)
        
        print "moved", move, j, "steps, now at", position

        if im:
            plt.figure(1)
            plt.savefig('images/2DPaths.png', dpi=900)
            plt.figure(2)
            plt.savefig('images/2DPointsKDE.png', dpi=900)
            plt.figure(3)
            plt.savefig('images/2DCone.png', dpi=900)
        
        raw_input("Press ENTER to advance to next move")
    return path



path = forcing(start, bounds, steps, stepSize, dims)
path = [[p[i] for p in path] for i in range(dims)]

plt.figure(1)
plt.clf()
ax = plt.gca(aspect = 'equal')
ax.set_title("Particle in a 2 dimensional box")
ax.set_xlim(bounds[0][0], bounds[0][1])
ax.set_ylim(bounds[1][0], bounds[1][1])
ax.plot(path[0], path[1], linewidth=0.1, color='k')
plt.show()
raw_input("Press ENTER to quit")
