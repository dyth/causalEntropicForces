#!/usr/bin/env python
"""as accurate an implementation as possible"""
import math, sys, os, json
import numpy as np

from monteCarloGaussianPaths import *



def totalVolume(logProbs):
    'calculate the volume fraction for a dimension'
    largest = max(logProbs)
    others = sum([math.exp(i - largest) for i in logProbs])
    others = math.log(1.0 + others)
    return largest - others


def entropicForce(pos):
    'calculate where the next step should be with mean of all samples'
    # sample and return first points and the log-likelihoods
    stdev = math.sqrt(variance)
    config = configuration(dims, stdev, valid, mass, randomStep)
    points, logProbs = monteCarloGaussianPaths(pos, samples, config, depth)
    # calculate mean of first step and the volume of the log-likelihoods
    mean = np.mean(points, axis=0)
    volume = [totalVolume(logProbs[i]) for i in range(dims)]
    # calculate the total entropic force
    total = [0.0 for _ in range(dims)]
    for j in range(samples):
        difference = points[j] - mean
        for i in range(dims):
            total[i] += difference[i] * (volume[i] - logProbs[i][j])
    return 4.0 * Tc * np.array(total) / (samples**2.0 * Tr * timeStep**2.0)


def forcing(pos, moved, path):
    'return path taken by forcing of particle, similar to the randomWalk'
    if moved == 0:
        return path
    else:
        newPos = pos + entropicForce(pos)
        if valid(path, newPos):
            path.append(newPos.tolist())
            moved -= 1
            pos = newPos
            print "moved", steps - moved, "steps, now at", newPos
    return forcing(pos, moved, path)



# load configuration properties
with open('config.json') as configFile:
    config = json.load(configFile)
    
# import environment
environment = str(config["game"])
sys.path.append(os.path.join(os.path.dirname(sys.path[0]), environment))
filename = '../' + environment + "/" + environment + '.py'
with open(filename) as f:
    exec(compile(f.read(), filename, "exec"))

# global entropic variables
exec("samples = + int(" + config["samples"] + ")")
exec("steps = int(" + config["steps"] + ")")
depth = tau / timeStep
variance = (kb * Tr * timeStep**2.0) / (4.0 * mass) # variance per step

# *** do causal entropic forcing, keep track of path ***
print "starting position at", start
path = [start.tolist()] + forcing(start, steps, [])
plot(path)
