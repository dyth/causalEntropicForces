#!/usr/bin/env python
"""Inspired by https://github.com/eholmgren/langevin"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import math

damping = 1.0


def step(u, v, environment):
    '''return next distance and speed timestep using Euler's Method'''
    #drag = -1 * damping * vi
    #solvent = np.random.normal(0, 2 * temperature * damping)
    DISTRIBUTION = norm(0.0, environment.AMPLITUDE)
    a = DISTRIBUTION.rvs(1) / environment.MASS
    # drag + solvent + a
    v += a * environment.TIMESTEP
    return u + v * environment.TIMESTEP, v


def random_walk(u, v, environment):
    'Runs all steps of the simulation'
    positions = [u]
    for _ in range(int(environment.TAU / environment.TIMESTEP)):
        u, v = step(u, v, environment)
        positions.append(u)
    return positions


def monte_carlo_path_sampling(u, v, environment):
    plt.figure()
    for _ in range(100):
        plt.plot(random_walk(u, v, environment))
    plt.show()
