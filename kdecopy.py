#!/usr/bin/env python
"""perform kernel density estimation on noughts and crosses"""

# Based on BSD licensed code by Jake VanderPlas

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


def estimate(X, bounds, number, Nx, Ny):
    'perform kernel density estimation on 2 dimensions'
    warnings.filterwarnings("ignore")
    Xgrid = np.vstack(map(np.ravel, np.meshgrid(np.linspace(bounds[0][0], bounds[0][1], Nx), np.linspace(bounds[1][0], bounds[1][1], Ny)))).T
    
    kde1 = KernelDensity(5, kernel='gaussian')
    log_dens1 = kde1.fit(X).score_samples(Xgrid)
    dens1 = log_dens1.reshape((Nx, Ny))
    return dens1


def plot(dens1, bounds, number):
    'plot using pyplot'
    ax.imshow(dens1, origin='lower', extent=(bounds[0][0], bounds[0][1], bounds[1][0], bounds[1][1]), cmap=plt.cm.binary)
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
#number = [b[1] - b[0] for b in bounds]
#print number, Nx, Ny
dens1 = estimate(X, bounds, 10, Nx, Ny)
plot(dens1, bounds, 10)
