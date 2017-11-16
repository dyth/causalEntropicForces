#!/usr/bin/env python
"""Inspired by https://github.com/eholmgren/langevin"""
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
import math


def step(u, environment):
    'compute next distance by Forward Euler'
    f = environment.DISTRIBUTION.rvs(environment.DIMS)
    pos = u + (f * (environment.TIMESTEP) ** 2.0) / environment.MASS
    return pos, environment.DISTRIBUTION.logpdf(f), f


def random_walk(u, environment):
    'Langevin random walk from force for TAU / TIMESTEP steps'
    positions, count = [u], int(environment.TAU / environment.TIMESTEP)
    logPr, force = 0.0, []
    while count != 0:
        u, lP, f = step(positions[-1], environment)
        # if valid then redo
        if environment.valid(positions, u):
            positions.append(u)
            count -= 1
            logPr += lP
            force.append(f)
    return positions, logPr, force[1] - force[0]


def monte_carlo_path_sampling(number, u, environment):
    'do number walks within environment with starting position u and velocity v'
    walks, logPr, forces = [], [], []
    for i in range(number):
        w, lP, initialForce = random_walk(u, environment)
        walks.append(w)
        logPr.append(lP)
        forces.append(initialForce)
    return walks, logPr, forces
