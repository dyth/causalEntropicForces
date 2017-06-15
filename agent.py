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
    points = np.vstack(map(np.ravel, np.meshgrid(np.linspace(xmin, xmax, Nx),
                                                np.linspace(ymin, ymax, Ny)))).T
    kde = KernelDensity(5, kernel='gaussian')
    return [kde.fit(X).score(point) for point in points]


def average(log_prob, points):
    for i in points:
        pass
