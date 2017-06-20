#!/usr/bin/env python
"""module for Monte Carlo Path Sampling"""
import random, math
from math import sqrt
from scipy.stats import norm


def randomStep(dims, delta, timeStep):
    'generate piecewise continous gaussian step'
    return norm.rvs(size=dims, scale=delta*sqrt(timeStep))


def randomWalk(walk, depth, dims, timeStep, delta, valid):
    """
    float delta : amount travelled per step. delta = sqrt(VAR/t)
    """
    if (depth == 0):
        # base case
        return walk
    else:
        # generate next step and add to current position
        step = randomStep(dims, delta, timeStep)
        point = [int(step[i] + walk[-1][i]) for i in range(dims)]
        # if invalid, do the computation again by recursion otherwise descend
        if (not valid(walk, point)):
            return randomWalk(walk, depth, dims, timeStep, delta, valid)
        else:
            walk.append(point)
            return randomWalk(walk, depth-1, dims, timeStep, delta, valid)


def monteCarloGaussianPaths(start, number, depth, dims, timeStep, delta, valid):
    'do number of monte carlo random walks at depth'
    walks = []
    for _ in range(number):
        walks.append(randomWalk([start], depth, dims, timeStep, delta, valid)[-1])
    return walks
