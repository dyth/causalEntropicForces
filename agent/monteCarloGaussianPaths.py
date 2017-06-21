#!/usr/bin/env python
"""module for Monte Carlo Path Sampling"""
from math import sqrt
from scipy.stats import norm
import numpy as np
import copy


class configuration:
    'struct preventing sesquipedalian function arguments'
    def __init__(self, depth, dims, stdev, valid):
        self.depth = depth 
        self.dims = dims
        self.stdev = stdev
        self.valid = valid


# TODO: ADD GAUSSIAN PROBABILITIES
        
def randomStep(dist, dims):
    'generate piecewise continous Gaussian step'
    return dist.rvs(size=dims)


def randomWalk(walk, config):
    'return list of Monte Carlo Weiner Process coordinates by recursion'
    # base case at 0, otherwise generate
    if config.depth == 0:
        return walk
    else:
        dist = norm(0.0, config.stdev)
        point = randomStep(dist, config.dims) + walk[-1]
        # if valid descend else redo
        if config.valid(walk, point):
            walk.append(point)
            config.depth -= 1
        return randomWalk(walk, config)

        
def monteCarloGaussianPaths(start, number, config):
    'do number of monte carlo random walks at depth'
    walks = []
    for _ in range(number):
        walks.append(randomWalk([start], copy.deepcopy(config))[-1])
    return walks
