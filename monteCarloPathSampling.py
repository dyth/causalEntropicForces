#!/usr/bin/env python
"""module for Monte Carlo Path Sampling"""
import random

def randomStep(dimensionality):
    'do a valid step in a random walk'
    # create random vector, normalise, then multiply by step size
    step = [random.uniform(-1.0, 1.0) for _ in dimensionality]
    magnitude = sum([i**2.0 for i in step])
    step = [stepSize * i / magnitude for i in step]
    return step
    

def randomWalk(depth, dimensionality):
    'do a random walk for depth steps'
    walk = []
    for _ in range(depth):
        walk.append(randomStep(dimensionality))
        while (not valid(walk)):
            walk[-1] = randomStep(dimensionality)
    return walk


def monteCarloPathSampling(number, depth, dimensionality):
    'do number of monte carlo random walks at depth'
    for _ in range(number):
        walk = randomWalk(depth, dimensionality)
