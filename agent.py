#!/usr/bin/env python
"""perform kernel density estimation on 2D grid"""
import numpy as np
import warnings
from numpy import array
#from scipy.spatial import cKDTree
from scipy.stats import gaussian_kde
from sklearn.neighbors import KernelDensity


def estimate(X, xmin, xmax, ymin, ymax, Nx, Ny):
    'perform kernel density estimation on 2 dimensions'
    # Based on BSD licensed code by Jake VanderPlas
    warnings.filterwarnings("ignore")
    Xgrid = np.vstack(map(np.ravel, np.meshgrid(np.linspace(xmin, xmax, Nx),
                                                np.linspace(ymin, ymax, Ny)))).T
    kde1 = KernelDensity(5, kernel='gaussian')
    log_prob = array([kde1.fit(X).score(point) for point in Xgrid])
    log_prob = X.shape[0] * log_prob.reshape((Ny, Nx))
    return dens1
