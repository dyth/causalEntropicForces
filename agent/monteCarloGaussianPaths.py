#!/usr/bin/env python
"""module for Monte Carlo Path Sampling"""
from math import sqrt
from scipy.stats import norm
import numpy as np
import copy


class configuration:
    'struct preventing sesquipedalian function arguments'
    def __init__(self, depth, dims, scale, valid):
        self.depth = depth 
        self.dims = dims
        self.scale = scale
        self.valid = valid


        
def randomStep(dims, scale):
    'generate piecewise continous Gaussian step'
    return norm.rvs(size=dims, scale=scale)


# TODO: TRANSLATE INTO NUMPY

def randomWalk(walk, config):
    'Monte Carlo random walk returning list of coordinates and '
    if config.depth == 0:
        # base case
        return walk
    else:
        # generate next step and add to current position
        step = randomStep(config.dims, config.scale)
        point = [int(step[i] + walk[-1][i]) for i in range(config.dims)]
        # if invalid, do the computation again by recursion otherwise descend
        if not config.valid(walk, point):
            return randomWalk(walk, config)
        else:
            walk.append(point)
            config.depth -= 1
            return randomWalk(walk, config)

        
def monteCarloGaussianPaths(start, number, config):
    'do number of monte carlo random walks at depth'
    walks = []
    for _ in range(number):
        walks.append(randomWalk([start], copy.deepcopy(config))[-1])
    return walks
