#!/usr/bin/env python
"""perform KDE over the state space"""
import numpy as np
from scipy.stats import gaussian_kde


def step(u, environment):
    'compute next distance by Forward Euler'
    force = [environment.DISTRIBUTION.rvs() for _ in range(environment.DIMS)]
    pos = u + (np.array(force) * environment.TIMESTEP ** 2.0) / environment.MASS
    return pos, force


def random_walk(u, environment):
    'Langevin random walk from force for TAU / TIMESTEP steps'
    walk, count, force = [u], int(environment.TAU / environment.TIMESTEP), None
    while count != 0:
        u, f = step(walk[-1], environment)
        # if valid then redo
        if environment.valid(walk, u):
            walk.append(u)
            count -= 1
            if force == None:
                force = f
    return walk[1:], np.array(force)


def monte_carlo_path_sampling(number, pos, environment):
    'return walks, forces of len(number) from pos in environment'
    tuples = [random_walk(pos, environment) for _ in range(number)]
    return [t[0] for t in tuples], [t[1] for t in tuples]


def log_volume_fractions(walks):
    'return log_volume_fractions on a set of random walks'
    points = []
    for walk in walks:
        for w in walk:
            points.append(w)
    kernel = gaussian_kde(np.array(points).T)
    return [sum([kernel.logpdf(w) for w in walk]) for walk in walks]


if __name__ == "__main__":
    from particleBox import ParticleBox
    numSamples, environment = 100, ParticleBox()
    pos = environment.start
    walks, f = monte_carlo_path_sampling(numSamples, pos, environment)
    print log_volume_fractions(walks)
    
