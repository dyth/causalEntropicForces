#!/usr/bin/env python
"""Inspired by https://github.com/eholmgren/langevin"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import math


def step(u, v, environment):
    'compute next distance and speed using Forward Euler'
    #DAMPING = 1.0 # between 0.0 and 1.0
    #drag = -1 * DAMPING * vi
    #solvent = np.random.normal(0, 2 * environment.TR * DAMPING)
    DISTRIBUTION = norm(0.0, environment.AMPLITUDE)
    a = DISTRIBUTION.rvs(1) / environment.MASS
    # drag + solvent + a
    #v += a * environment.TIMESTEP
    return u + a * (environment.TIMESTEP) ** 2.0 / 2.0, v#v * environment.TIMESTEP, v


def random_walk(u, v, environment):
    'Langevin random walk from force for TAU / TIMESTEP steps'
    positions = [u]
    for _ in range(int(environment.TAU / environment.TIMESTEP)):
        u, v = step(u, v, environment)
        positions.append(u)
    return positions


def monte_carlo_path_sampling(number, u, v, environment):
    'do number walks within environment with starting position u and velocity v'
    walks = [random_walk(u, v, environment) for _ in range(number)]
    plt.figure()
    for w in walks:
        plt.plot(w)
    plt.show()
    return walks
