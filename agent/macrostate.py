#!/usr/bin/env python
"""Model Based Reflex Agent with Entropic Forcing Updates"""
from particleBox import ParticleBox
from microstate import *
from sys import exit


def entropic_forcing(logProbs, environment, forces):
    'calculate the path integral and determine the next best move'
    pathIntegral = sum([f*logProbs[i] for i, f in enumerate(forces)])
    nom = 2.0 * environment.TC * pathIntegral * environment.TIMESTEP ** 2.0
    denom = 2.0 * environment.TR * environment.MASS * len(forces)
    return nom / denom 


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
        exit()
    print pos
    path.append(pos)
