#!/usr/bin/env python
"""module for Monte Carlo Path Sampling"""
import math
from scipy.stats import norm
import numpy as np


class configuration:
    'class prevents sesquipedalian invocations'
    
    def __init__(self, dims, stdev, valid):
        self.dims = dims
        self.valid = valid
        self.dist = norm(0.0, stdev)

        
    def randomStep(self, pos):
        'generate piecewise continuous Gaussian step and its probability'
        point = self.dist.rvs(size=self.dims)
        return pos + point, self.dist.cdf(point) - self.dist.cdf(point - 1.0)



def randomWalk(walk, logProb, config, depth):
    'return list of Monte Carlo Weiner Process coordinates by recursion'
    # base case at 0, otherwise generate
    if depth == 0:
        #print logProb
        return walk[-1], logProb
    else:
        point, p = config.randomStep(walk[-1])
        # if valid descend else redo
        if config.valid(walk, point):
            #logProb += np.array([math.log(i) for i in p])
            #print p
            walk.append(point)
            depth -= 1
        return randomWalk(walk, logProb, config, depth)

        
def monteCarloGaussianPaths(start, number, config, depth):
    'do number of monte carlo random walks at depth'
    walks = []
    for _ in range(number):
        walks.append(randomWalk([start], 0.0, config, depth)[0])
    return walks
