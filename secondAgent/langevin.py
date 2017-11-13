#!/usr/bin/env python
"""Inspired by https://github.com/eholmgren/langevin"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm


damping = 1.0
DISTRIBUTION = norm(0.0, 1.0)


def step(xi, vi, temperature, damping):
    '''return next distance and speed timestep using Euler's Method'''
    #drag = -1 * damping * vi
    #solvent = np.random.normal(0, 2 * temperature * damping)
    fpotential = DISTRIBUTION.rvs(1)
    # drag + solvent + fpotential
    return xi + vi * timestep, vi + fpotential * timestep


def random_walk(p, v, totaltime, timestep, temperature, damping):
    'Runs all steps of the simulation'
    positions = [p]

    for s in range(int(totaltime / timestep)):
        p, v = step(p, v, temperature, damping)
        positions.append(p)

    plt.figure()
    plt.plot(positions)
    plt.show()
    return positions

    
if __name__ == '__main__':
    position = 0.0
    velocity = 0.0
    temperature = 1.0
    timestep = 0.025
    totaltime = 10.0
    random_walk(0.0, velocity, totaltime, timestep, temperature, damping)
