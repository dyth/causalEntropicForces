#!/usr/bin/env python
"""perform KDE per dimension then get result"""
import numpy as np
from scipy.stats import gaussian_kde


def step(u, environment):
    'compute next distance by Forward Euler'
    force = [environment.DISTRIBUTION.rvs() for _ in range(environment.DIMS)]
    pos = u + (np.array(force) * environment.TIMESTEP ** 2.0) / environment.MASS
    return pos, force


def random_walk(u, environment):
    'Langevin random walk from force for TAU / TIMESTEP steps'
    walk, count, force = [u], int(environment.TAU / environment.TIMESTEP), []
    while count != 0:
        u, f = step(walk[-1], environment)
        # if valid then redo
        if environment.valid(walk, u):
            walk.append(u)
            count -= 1
            force.append(f)
    return walk, np.array(force[1]) - np.array(force[0])


def monte_carlo_path_sampling(number, pos, environment):
    'do number walks within environment with starting position u and velocity v'
    walks, forces = [], []
    for i in range(number):
        w, initialForce = random_walk(pos, environment)
        walks.append(w)
        forces.append(initialForce)
    return walks, forces


def log_volume_fractions(walks):
    'return log_volume_fractions of a set of random walks'
    walks = np.array(walks).T
    print walks.shape
    logPr = []
    kdes = [gaussian_kde(w[1:]) for w in walks]
    for j in range(len(walks[0].T)):
        logPr.append([k.logpdf(walks[i].T[j][1:]) for i, k in enumerate(kdes)])
    return np.array(logPr)


from particleBox import ParticleBox
path, numSamples = [], 10000
environment = ParticleBox()
pos = environment.start
walks, f = monte_carlo_path_sampling(numSamples, pos, environment)
print log_volume_fractions(walks)

