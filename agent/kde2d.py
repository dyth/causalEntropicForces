#!/usr/bin/env python
"""perform KDE over the state space"""
import numpy as np
from scipy.stats import gaussian_kde
import matplotlib.pyplot as pl


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


def log_volume_fractions(points):
    'return log_volume_fractions on a set of random walks'
    points = np.array(points).T
    kernel = gaussian_kde(points)

    xmin, xmax = 0, 400
    ymin, ymax = 0, 80

    # Peform the kernel density estimate
    xx, yy = np.mgrid[xmin:xmax:100j, ymin:ymax:100j]
    positions = np.vstack([xx.ravel(), yy.ravel()])
    f = np.reshape(kernel(positions).T, xx.shape)
    
    fig = pl.figure()
    ax = fig.gca()
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    # Contourf plot
    cfset = ax.contourf(xx, yy, f, cmap='Blues')
    ## Or kernel density estimate plot instead of the contourf plot
    ax.imshow(np.rot90(f), cmap='Blues', extent=[xmin, xmax, ymin, ymax])
    # Contour plot
    cset = ax.contour(xx, yy, f, colors='k')
    # Label plot
    ax.clabel(cset, inline=1, fontsize=10)
    ax.set_xlabel('Y1')
    ax.set_ylabel('Y0')
    pl.axes().set_aspect('equal', 'datalim')
    pl.show()


if __name__ == "__main__":
    from particleBox import ParticleBox
    path, numSamples = [], 1000
    environment = ParticleBox()
    pos = environment.start
    walks, f = monte_carlo_path_sampling(numSamples, pos, environment)
    points = []
    for walk in walks:
        for w in walk:
            points.append(w)
    log_volume_fractions(points)
