#!/usr/bin/env python
"""module for Monte Carlo Path Sampling of random walks by the Wiener Process"""
import math
from scipy.stats import norm
import numpy as np


class configuration:
    'class prevents sesquipedalian invocations'
    
    def __init__(self, dims, stdev, valid, mass):
        self.dims = dims
        self.valid = valid
        self.dist = norm(0.0, stdev)
        self.mass = mass

        
    def randomStep(self, pos):
        'generate piecewise continuous Gaussian step and its probability'
        point = self.dist.rvs(size=self.dims)
        #point = np.array([point[i] / self.mass for i in range(self.dims)])
        return pos + point, self.dist.logpdf(point)



def randomWalk(walk, logProb, config, depth):
    'return list of Monte Carlo Weiner Process coordinates by recursion'
    # base case at 0, otherwise generate
    if depth == 0:
        return walk[-1], logProb
    else:
        point, p = config.randomStep(walk[-1])
        # if valid descend else redo
        if config.valid(walk, point):
            logProb += p
            walk.append(point)
            depth -= 1
        return randomWalk(walk, logProb, config, depth)


def monteCarloGaussianPaths(start, samples, config, depth):
    'do number of monte carlo random walks at depth'
    points, logProbs = [], [[] for _ in range(config.dims)]
    for _ in range(samples):
        point, logProb = randomWalk([start], 0.0, config, depth)
        points.append(point)
        for i in range(config.dims):
            logProbs[i].append(logProb[i])
    return points, logProbs
