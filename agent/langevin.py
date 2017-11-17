#!/usr/bin/env python
"""Inspired by https://github.com/eholmgren/langevin"""
import numpy as np
from scipy.stats import norm
import math


def step(u, environment):
    'compute next distance by Forward Euler'
    force = [environment.DISTRIBUTION.rvs() for _ in range(environment.DIMS)]
    logProb = [environment.DISTRIBUTION.logpdf(f) for f in force]
    pos = u + (np.array(force) * environment.TIMESTEP ** 2.0) / environment.MASS
    return pos, logProb, force


def random_walk(u, environment):
    'Langevin random walk from force for TAU / TIMESTEP steps'
    walk, count = [u], int(environment.TAU / environment.TIMESTEP)
    logPr, force = np.zeros(environment.DIMS), None
    while count != 0:
        u, lP, f = step(walk[-1], environment)
        # if valid then redo
        if environment.valid(walk, u):
            walk.append(u)
            count -= 1
            logPr += lP
            if force == None:
                force = f
    return walk, logPr, np.array(force)


def monte_carlo_path_sampling(number, pos, environment):
    'do number walks within environment with starting position u and velocity v'
    walks, logPr, forces = [], [], []
    for i in range(number):
        w, lP, initialForce = random_walk(pos, environment)
        walks.append(w)
        logPr.append(lP)
        forces.append(initialForce)
    return walks, logPr, forces
