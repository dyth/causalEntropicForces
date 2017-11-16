#!/usr/bin/env python
"""Model Based Reflex Agent with Entropic Forcing Updates"""
from particleBox import ParticleBox
from langevin import *
from scipy.stats import norm
import math, sys


def entropic_forcing(logProbs, numSamples, environment, forces):
    'calculate the path integral and determine the next best move'
    path_integral = 0.0
    for i, f in enumerate(forces):
        # calculate the partial volume v and then weighted sum to path_integral
        v = np.log(sum([np.exp(lP - logProbs[i]) for lP in logProbs]))
        path_integral += f * v
    nom = 2.0 * environment.TC * path_integral * environment.TIMESTEP ** 2
    denom = environment.TR * numSamples * environment.MASS
    return nom / denom


plot = False
path, numSamples = [], 250
environment = ParticleBox()
pos = environment.start
print pos
while True:
    walks, logProbs, f = monte_carlo_path_sampling(numSamples, pos, environment)

    if plot:
        plt.figure()
        for w in walks:
            plt.plot([wi[0] for wi in w], [wi[1] for wi in w])
        plt.show()
        
    move = entropic_forcing(logProbs, numSamples, environment, f)
    pos += move
    if not environment.valid(path, pos):
        print "Error: Agent in invalid environment state,", pos
        sys.exit()
    print pos
    path.append(pos)
