#!/usr/bin/env python
"""Model Based Reflex Agent with Entropic Forcing Updates"""
from particleBox import ParticleBox
from langevin import *
import matplotlib.pyplot as plt
from scipy.stats import norm
import numpy as np


def entropic_forcing(logProbs, environment, forces):
    'calculate the path integral and determine the next best move'
    pathIntegral = 0.0
    for i, f in enumerate(forces):
        # calculate the partial volume v and then weighted sum to path_integral
        v = np.log(sum([np.exp(lP - logProbs[i]) for lP in logProbs]))
        pathIntegral += np.multiply(f, v)
    nom = 2.0 * environment.TC * pathIntegral * environment.TIMESTEP ** 2
    denom = environment.TR * (len(forces) + 1) * environment.MASS
    return nom / denom


def debounce_entropic_forcing(u, environment):
    'calculate the path integral until it converges'
    walks, logPr, forces = [], [], []
    pathIntegral, pI = np.array([None, 2.0]), np.array([1.0, 1.0])
    while not np.array_equal(pathIntegral, pI):
        pI = pathIntegral
        w, lP, initialForce = random_walk(u, environment)
        walks.append(w)
        logPr.append(lP)
        forces.append(initialForce)
        pathIntegral = entropic_forcing(logPr, environment, forces)
        print len(forces), pathIntegral
    return pathIntegral



plot = True
path, numSamples = [], 1000
environment = ParticleBox()
pos = environment.start
print pos
"""
debounce_entropic_forcing(pos, environment)

"""
while True:
    walks, logProbs, f = monte_carlo_path_sampling(numSamples, pos, environment)
    move = entropic_forcing(logProbs, environment, f)
    pos += move
    if not environment.valid(path, pos):
        print "Error: Agent in invalid environment state,", pos
        sys.exit()
    print pos
    path.append(pos)


