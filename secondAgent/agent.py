#!/usr/bin/env python
"""Model Based Reflex Agent with Entropic Forcing Updates"""
from particleBox import ParticleBox
from langevin import *
from scipy.stats import norm
import math


def entropic_forcing(walks, logProbs, numSamples):
    'calculate the path integral and determine the next best move'
    path_integral = 0.0
    for i, w in enumerate(walks):
        # calculate the partial volume v and then weighted sum to path_integral
        v = np.log(sum([np.exp(lP - logProbs[i]) for lP in logProbs]))
        path_integral += (w[i][1] - w[i][0]) * v
    return 2 * Tc * path_integral / (Tr * numSamples * 100)


environment = ParticleBox()
monte_carlo_path_sampling(100, 0.0, 0.0, environment)
"""
distribution = norm(mean, stdev)
config = Configuration(distribution, dims, valid)
path = []
numSamples = 100
depth = tau / timeStep
pos = start
print pos
while True:
    walks, logProbs = monteCarloGaussianPaths(pos, numSamples, config, depth)
    move = entropic_forcing(walks, logProbs, numSamples)
    pos += move
    if not valid(path, pos):
        print "Error: Agent in invalid environment state,", pos
        sys.exit()
    print pos
    path.append(pos)
"""
