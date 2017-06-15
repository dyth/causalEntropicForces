#!/usr/bin/env python
"""particle in a box which drifts towards the centre"""
import matplotlib.pyplot as plt
from numpy import array

from monteCarloPathSampling import *
from kde import *
from agent import *


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


if __name__ == "__main__":
    X = monteCarloPathSampling(start, 100, depth, dims, stepSize, valid)

    plt.figure()
    ax = plt.gca(aspect = 'equal')
    ax.set_title("KDE and points")
    ax.set_xlim(bounds[0][0], bounds[0][1])
    ax.set_ylim(bounds[1][0], bounds[1][1])
    # strangely, after KDE, the axes have swapped, so plot points swapped round
    [plt.plot(i[1], i[0], "o") for i in X]

    X = array(X)

    xmin, xmax = bounds[0][0], bounds[0][1]
    ymin, ymax = bounds[1][0], bounds[1][1]
    Nx, Ny = xmax - xmin, ymax - ymin

    dens1 = estimate(X, xmin, xmax, ymin, ymax, Nx, Ny)
    plot(dens1, xmin, xmax, ymin, ymax)
    print dens1.T
