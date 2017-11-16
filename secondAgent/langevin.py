#!/usr/bin/env python
"""Inspired by https://github.com/eholmgren/langevin"""
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
import math


def step(u, environment):
    'compute next distance by Forward Euler'
    force = [environment.DISTRIBUTION.rvs() for _ in range(environment.DIMS)]
    logProb = [environment.DISTRIBUTION.logpdf(f) for f in force]
    pos = u + (np.array(force) * environment.TIMESTEP ** 2.0) / environment.MASS
    return pos, logProb, force


def random_walk(u, environment):
    'Langevin random walk from force for TAU / TIMESTEP steps'
    positions, count = [u], int(environment.TAU / environment.TIMESTEP)
    logPr, force = np.zeros(environment.DIMS), []
    while count != 0:
        u, lP, f = step(positions[-1], environment)
        # if valid then redo
        if environment.valid(positions, u):
            positions.append(u)
            count -= 1
            logPr += lP
            force.append(f)
    return positions, logPr, np.array(force[1]) - np.array(force[0])


def monte_carlo_path_sampling(number, pos, environment):
    'do number walks within environment with starting position u and velocity v'
    walks, logPr, forces = [], [], []
    for i in range(number):
        w, lP, initialForce = random_walk(pos, environment)
        walks.append(w)
        logPr.append(lP)
        forces.append(initialForce)
    return walks, logPr, forces
