#!/usr/bin/env python
"""perform kernel density estimation on 2D grid"""
import numpy as np
import warnings
from numpy import array
from scipy.spatial import cKDTree
from scipy.stats import gaussian_kde
from sklearn.neighbors import KernelDensity

from monteCarloPathSampling import *
from particleBox import *


def estimate(X, bounds, number):
    'return log of kernel density probability on 2 dimensions'
    warnings.filterwarnings("ignore")
    xs = np.linspace(bounds[0][0], bounds[0][1], number[0])
    ys = np.linspace(bounds[1][0], bounds[1][1], number[1])
    points = np.vstack(map(np.ravel, np.meshgrid(xs, ys))).T
    kde = KernelDensity(5, kernel='gaussian')
    return [kde.fit(X).score(point).tolist() for point in points], points


def average(logProb, points, position):
    'take weighted average of logProb and points offset to find mean outcome'
    mean = [0.0, 0.0]
    points = [point - position for point in points]
    for index in range(len(points)):
        mean += logProb[index] * points[index]
    return [m / float(len(points)) for m in mean]
    

def steps(position, bounds, number):
    'calculate where the next step should be'
    points = monteCarloPathSampling(start, 200, depth, dims, stepSize, valid)
    points = array(points)
    logProb, allPoints = estimate(points, bounds, number)
    mean = average(logProb, allPoints, position)
    magnitude = sum([m**2 for m in mean])
    move = [-stepSize * m / magnitude for m in mean]
    return move


def forcing(position, bounds, steps, dims):
    number = [b[1] - b[0] for b in bounds]
    move = steps(position, bounds, number)
    position = [position[i] += move[i] for i in range(dims))]


forcing(start, 100, 100, dims)
