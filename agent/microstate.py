#!/usr/bin/env python
"""perform KDE over the state space"""
import numpy as np
from scipy.stats import gaussian_kde
import matplotlib.pyplot as pl


def step(u, environment):
    'compute next distance by Forward Euler'
    force = environment.AMPLITUDE*environment.DISTRIBUTION.rvs(environment.DIMS)
    pos = u + (np.array(force) * environment.TIMESTEP) / environment.MASS
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
    return walk[1:], force


def monte_carlo_path_sampling(number, pos, environment):
    'return walks, forces of len(number) from pos in environment'
    tuples = [random_walk(pos, environment) for _ in range(number)]
    return [t[0] for t in tuples], [t[1] for t in tuples]


def log_volume_fractions(walks):
    'return log_volume_fractions on a set of random walks'
    points = [w[-1] for w in walks]
    kernel = gaussian_kde(np.array(points).T)
    """
    # plot the kernel density estimate
    xmin, xmax = 0, 400
    ymin, ymax = 0, 80
    
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
    """
    return [kernel.logpdf(w[-1]) for w in walks]


if __name__ == "__main__":
    from particleBox import ParticleBox
    numSamples, environment = 500, ParticleBox()
    pos = environment.start
    walks, f = monte_carlo_path_sampling(numSamples, pos, environment)
    print log_volume_fractions(walks)
    
