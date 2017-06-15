#!/usr/bin/env python
"""perform kernel density estimation on noughts and crosses"""
import numpy as np
import warnings
from numpy import array
from matplotlib import pyplot as plt
from matplotlib.colors import LogNorm
from scipy.spatial import cKDTree
from scipy.stats import gaussian_kde
from sklearn.neighbors import KernelDensity

from monteCarloPathSampling import *
from particleBox import *


def estimate(points, bounds, number):
    'return log of kernel density probability on 2 dimensions'
    warnings.filterwarnings("ignore")
    xs = np.linspace(bounds[0][0], bounds[0][1], number[0])
    ys = np.linspace(bounds[1][0], bounds[1][1], number[1])
    cs = np.vstack(map(np.ravel, np.meshgrid(xs, ys))).T
    kde = KernelDensity(5, kernel='gaussian')
    return [kde.fit(points).score(c).tolist() for c in cs], cs


def plot(density, bounds, number):
    'plot points and KDE'
    plt.figure()
    ax = plt.gca(aspect = 'equal')
    ax.set_title("KDE and points")
    ax.set_xlim(bounds[0][0], bounds[0][1])
    ax.set_ylim(bounds[1][0], bounds[1][1])
    # plot visted points
    for point in points:
        plt.plot(point[0], point[1], "o")
    extent = (bounds[0][0], bounds[0][1], bounds[1][0], bounds[1][1])
    # plot density
    density = array(density).reshape(tuple(reversed(number)))
    ax.imshow(density, origin='lower', extent=extent, cmap=plt.cm.binary)
    plt.show()


    
if __name__ == "__main__":
    points = monteCarloPathSampling(start, 100, depth, dims, stepSize, valid)
    points = array(points)
    number = [b[1] - b[0] for b in bounds]
    density, _ = estimate(points, bounds, number)
    plot(density, bounds, number)
