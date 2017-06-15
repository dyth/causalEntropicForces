#!/usr/bin/env python
"""module for Monte Carlo Path Sampling"""
import random, math


def randomStep(dims, stepSize):
    'do a valid step in a random walk'
    # create random vector, normalise, then multiply by step size
    step = [random.uniform(-1.0, 1.0) for _ in range(dims)]
    magnitude = math.sqrt(sum([i**2.0 for i in step]))
    step = [stepSize * i / magnitude for i in step]
    magnitude = sum([i**2.0 for i in step])
    return step
    

def randomWalk(walk, depth, dims, stepSize, valid):
    'do a random walk for depth steps'
    if (depth == 0):
        # base case
        return walk
    else:
        # generate next step and add to current position
        step = randomStep(dims, stepSize)
        point = [int(step[i] + walk[-1][i]) for i in range(dims)]
        if (not valid(walk, point)):
            # if invalid, do the computation again by recursion
            return randomWalk(walk, depth, dims, stepSize, valid)
        else:
            # if valid, then append to history, then recurse
            walk.append(point)
            return randomWalk(walk, depth-1, dims, stepSize, valid)


def monteCarloPathSampling(start, number, depth, dims, stepSize, valid):
    'do number of monte carlo random walks at depth'
    return [randomWalk([start], depth, dims, stepSize, valid)[-1] for _ in range(number)]
