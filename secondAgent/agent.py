#!/usr/bin/env python
"""Model Based Reflex Agent with Entropic Forcing Updates"""
from particleBox import *
from scipy.stats import norm


def entropic_forcing(start, walks, logProbs):
    'calculate the path integral and determine the next best move'
    return move


distribution = norm(mean, stdev)
config = Configuration(dims, valid)
path = []
while True:
    walks, logProbs = monteCarloGaussianPaths(start, nosamples, config, depth)
    move = entropic_forcing(start, walks, logProbs)
    path.append(move)
    start += move
