#!/usr/bin/env python
"""Inspired by https://github.com/eholmgren/langevin"""
import numpy as np
import matplotlib.pyplot as plt
import math


def step(u, environment):
    'compute next distance by Forward Euler'
    f = environment.DISTRIBUTION.rvs(environment.DIMS)
    a = f / environment.MASS
    return u + a * (environment.TIMESTEP) ** 2.0, environment.DISTRIBUTION.logpdf(f)


def random_walk(u, environment):
    'Langevin random walk from force for TAU / TIMESTEP steps'
    positions = [u]
    count = 0
    while count != int(environment.TAU / environment.TIMESTEP):
        u, logPr = step(positions[-1], environment)
        if environment.valid(positions, u):
            positions.append(u)
            count += 1
    return positions


def monte_carlo_path_sampling(number, u, environment):
    'do number walks within environment with starting position u and velocity v'
    plt.figure()
    walk = [random_walk(u, environment) for _ in range(number)]
    for w in walk:
        plt.plot([wi[0] for wi in w], [wi[1] for wi in w])
    plt.show()
