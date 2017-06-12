#!/usr/bin/env python
"""perform kernel density estimation on noughts and crosses"""
import matplotlib.pyplot as plt

from lightCone2d import *


print "matplotlib finished building"
ax = plt.gca()
ax.set_title("Sampling points for Kernel Density Estimation")
ax.set_xlabel("First Coordinate")
ax.set_ylabel("Second Coordinate")
plt.ion()
plt.show()
while True:
    xs, ys, winner = randomWalk(initialBoard, 1, [0], [0])
    xs = historyToEncoding([0], xs, 1)
    ys = historyToEncoding([0], ys, 1)
    x = centreLight(xs)[-1]
    y = centreLight(ys)[-1]
    colour = 'g' if (winner == 1) else 'r'
    plt.plot(x, y, "o", c = colour)
    plt.draw()
    plt.pause(0.01)
