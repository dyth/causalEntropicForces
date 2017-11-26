#!/usr/bin/env python
"""Model Based Reflex Agent with Entropic Forcing Updates"""
from particleBox import ParticleBox
from microstate import *
from scipy.stats import norm
import numpy as np
import sys


def entropic_forcing(logProbs, environment, forces):
    'calculate the path integral and determine the next best move'
    pathIntegral = sum([f*logProbs[i] for i, f in enumerate(forces)])
    nom = 2.0 * environment.TC * pathIntegral * environment.TIMESTEP ** 2.0
    denom = 2.0 * environment.TR * environment.MASS * len(forces)
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


path, numSamples = [], 500
environment = ParticleBox()
pos = environment.start
print pos
while True:
    walks, f = monte_carlo_path_sampling(numSamples, pos, environment)
    logProbs = log_volume_fractions(walks)
    pos -= entropic_forcing(logProbs, environment, f)
    if not environment.valid(path, pos):
        print "Error: Agent in invalid environment state,", pos
        sys.exit()
    print pos
    path.append(pos)
