#!/usr/bin/env python
"""perform kernel density estimation"""
import numpy as np
import warnings
from numpy import array
from matplotlib import pyplot as plt
from matplotlib.colors import LogNorm
from scipy.spatial import cKDTree
from scipy.stats import gaussian_kde
from sklearn.neighbors import KernelDensity


def estimate(points, bounds, number):
    'return log of kernel density probability on 2 dimensions'
    warnings.filterwarnings("ignore")
    xs = np.linspace(bounds[0][0], bounds[0][1], number[0])
    ys = np.linspace(bounds[1][0], bounds[1][1], number[1])
    cs = np.vstack(map(np.ravel, np.meshgrid(xs, ys))).T
    kde = KernelDensity(5, kernel='gaussian')
    return [kde.fit(points).score(c).tolist() for c in cs], cs


def average(logProb, cs, position):
    'take weighted average of logProb and points offset to find mean outcome'
    mean = array([0.0, 0.0])
    points = array([c - position for c in cs])
    for index in range(len(cs)):
        mean += logProb[index] * cs[index]
    return [m / float(len(points)) for m in mean]
