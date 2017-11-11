#!/usr/bin/env python
"""Monte Carlo Random Walks"""
import math, sys
from scipy.stats import norm
import numpy as np


class Configuration:
    'struct preventing sesquipedalian invocations'
    def __init__(self, distribution, dimensions, valid):
        self.distribution = distribution
        self.dimensions = dimensions
        self.valid = valid


def random_step(distribution, dimensions):
    'generate piecewise continuous Gaussian (Weiner) step and log-likelihood'
    point = distribution.rvs(dimensions)
    return point, distribution.logpdf(point)


def random_walk(walk, logProb, config, depth):
    'return list of Monte Carlo Weiner Process coordinates by recursion'
    # if base, return trajectory and logarithimic probability
    while depth > 0:
        offset, logP = random_step(config.distribution, config.dimensions)
        point = walk[-1] + offset
        # if valid descend else redo
        if config.valid(walk, point):
            logProb += logP
            walk.append(point)
            depth -= 1
    return walk, logProb


def monteCarloGaussianPaths(start, numSamples, config, depth):
    'do nosamples of random walks at depth from start'
    walks, logProbs = [], []
    for i in range(numSamples):
        w, lP = random_walk([start], 0.0, config, depth)
        walks.append(w)
        logProbs.append(lP)
    return walks, logProbs


if __name__ == "__main__":
    mean = 0.0
    stdev = 1.0
    distribution = norm(mean, stdev)

    dimensions = 2

    length = 400.0
    bounds = ((0.0, length), (0.0, length/5.0))
    def valid(walk, point):
        'determine whether a walk is valid'
        if ((point[0] < bounds[0][0]) or (point[0] > bounds[0][1]) or
                (point[1] < bounds[1][0]) or (point[1] > bounds[1][1])):
            return False
        else:
            return True
    
    config = Configuration(distribution, dimensions, valid)
    walks, logprob =  random_walk([np.array([0.0, 0.0])], 0.0, config, 2)
    print walks
    print logprob
