#!/usr/bin/env python
"""recreation of particle in a box example"""
from monteCarloPathSampling import *

stepSize = 5.0
depth = 1
start = [-50.0, 0.0]
bounds = ((-100.0, 100.0), (-100.0, 100.0))
dimensionality = len(bounds)


def valid(walk, p):
    'determine whether a walk is valid'
    if (p[0] < bounds[0][0]) or (p[1] > bounds[0][1]) or (p[0] < bounds[1][0]) or (p[1] > bounds[1][1]):
        return False
    else:
        return True



while True:
     print randomWalk([start], depth, dimensionality, stepSize, valid)
