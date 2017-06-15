#!/usr/bin/env python
"""perform kernel density estimation on noughts and crosses"""

# Based on BSD licensed code by Jake VanderPlas

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.colors import LogNorm
from scipy.spatial import cKDTree
from scipy.stats import gaussian_kde
from sklearn.neighbors import KernelDensity

from astroML.datasets import fetch_great_wall


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
    ax = plt.gca(aspect = 'equal')
    ax.imshow(dens1.T, origin='lower', norm=LogNorm(),
            extent=(ymin, ymax, xmin, xmax), cmap=plt.cm.binary)
    ax.set_xlim(ymin, ymax - 0.01)
    ax.set_ylim(xmin, xmax)
    plt.show()


    
if __name__ == "__main__":
    # Fetch the great wall data
    X = fetch_great_wall()
    print type(X), len(X), len(X[0]), type(X[0]), type(X[0][0])

    # Create the grid on which to evaluate the results
    Nx = 50
    Ny = 125
    xmin, xmax = (-375, -175)
    ymin, ymax = (-300, 200)
    estimate(X, xmin, xmax, ymin, ymax, Nx, Ny)
    plot(dens1, xmin, xmax, ymin, ymax)
