#!/usr/bin/env python
"""Inspired by https://github.com/eholmgren/langevin"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm


position = 0.0
velocity = 0.0
temperature = 1.0
damping = 1.0
timestep = 0.025
totaltime = 10.0


DISTRIBUTION = norm(0.0, 1.0)


def step(xi, vi, temperature, damping):
    '''Calculate one timestep for x and v using Euler's Method'''

    drag = -1 * damping * vi
    solvent = np.random.normal(0, 2 * temperature * damping)
    fpotential = DISTRIBUTION.rvs(1)

    dvdt = drag + solvent + fpotential
    vj = vi + dvdt * timestep
    xj = xi + vi * timestep
    return xj, vj


def run(position, velocity, totaltime, timestep, temperature, damping):
    '''Runs all steps of the simulation'''

    iters = int(totaltime / timestep)
    
    xi, vi = position, velocity
    x, v = [xi], [vi]
    t = [0.0]
    for s in range(iters):
        xi, vi = step(xi, vi)
        ti = (s + 1) * timestep
        x.append(xi)
        v.append(vi)
        t.append(ti)

    fig = plt.figure()

    ax = fig.add_subplot(111)
    ax2 = ax.twinx()

    time = np.linspace(0, totaltime, len(x))
    l1 = ax.plot(time, x, 'b', label='position')
    l2 = ax2.plot(time, v, 'g', label='velocity')
    
    ax.set_title('Trajectory')
    ax.set_xlabel('Time')
    ax.set_ylabel('Position')
    ax2.set_ylabel('Velocity')
    
    lns = l1+l2
    labs = [l.get_label() for l in lns]
    ax.legend(lns, labs, loc=3)
    
    plt.show()
    
if __name__ == '__main__':
    run(position, velocity, totaltime, timestep, temperature, damping)


