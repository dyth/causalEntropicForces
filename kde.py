#!/usr/bin/env python
"""perform kernel density estimation on noughts and crosses"""

# Based on BSD licensed code by Jake VanderPlas

import numpy as np
from numpy import array
from matplotlib import pyplot as plt
from matplotlib.colors import LogNorm
from scipy.spatial import cKDTree
from scipy.stats import gaussian_kde
from sklearn.neighbors import KernelDensity

from monteCarloPathSampling import *
from particleBox import *


def estimate(X, xmin, xmax, ymin, ymax, Nx, Ny):
    'perform kernel density estimation on 2 dimensions'
    Xgrid = np.vstack(map(np.ravel, np.meshgrid(np.linspace(xmin, xmax, Nx),
                                                np.linspace(ymin, ymax, Ny)))).T
    kde1 = KernelDensity(5, kernel='gaussian')
    log_dens1 = kde1.fit(X).score_samples(Xgrid)
    dens1 = X.shape[0] * np.exp(log_dens1).reshape((Ny, Nx))
    return dens1


def plot(dens1, xmin, xmax, ymin, ymax):
    'plot using pyplot'
    ax.imshow(dens1, origin='lower', norm=LogNorm(),
            extent=(xmin, xmax, ymin, ymax), cmap=plt.cm.binary)
    plt.show()



X = monteCarloPathSampling(start, 100, depth, dims, stepSize, valid)

plt.figure()
ax = plt.gca(aspect = 'equal')
ax.set_title("KDE and points")
ax.set_xlim(bounds[0][0], bounds[0][1])
ax.set_ylim(bounds[1][0], bounds[1][1])
[plt.plot(i[0], i[1], "o") for i in X]

X = array(X)

xmin, xmax, ymin, ymax = bounds[0][0], bounds[0][1], bounds[1][0], bounds[1][1]
Nx, Ny = xmax - xmin, ymax - ymin

dens1 = estimate(X, xmin, xmax, ymin, ymax, Nx, Ny)
plot(dens1, xmin, xmax, ymin, ymax)
