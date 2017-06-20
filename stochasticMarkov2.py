#!/usr/bin/env python
"""stochastic path sampling with Weiner process
   Output markov chain probability output"""
import numpy as np
from pylab import plot, show, grid, axis, xlabel, ylabel, title

from math import sqrt
from scipy.stats import norm

from particleBox import *


def normalStep(delta, dt, dims):
    'generate piecewise continous gaussian step'
    return norm.rvs(size=dims, scale=delta*sqrt(dt))


def brownian(position, number, dt, delta):
    """
    int number  : number of iterations
    float dt    : time step
    float delta : amount travelled per step. VAR = delta**2*t
    """
    

    
def brownian(x0, n, dt, delta, out=None):
    'Monte Carlo Wiener process, return cumulative sum of stochastic gaussians'
    x0 = np.asarray(x0)

    # generate len(x0) gaussian samples
    r = norm.rvs(size=x0.shape + (n,), scale=delta*sqrt(dt))
    
    # create output if it does not exists
    if out is None:
        out = np.empty(r.shape)

    # cumulative sum
    np.cumsum(r, axis=-1, out=out)
    out += np.expand_dims(x0, axis=-1)
    return out



# The Wiener process parameter: 
delta = 0.25
# Total time.
T = 10.0
# Number of steps.
N = 10
# Time step size
dt = T/N
# Initial values of x.
x = np.empty((2, N+1))
x[:, 0] = 0.0

brownian(x[:,0], N, dt, delta, out=x[:,1:])



# Plot the 2D trajectory, mark the start and end points
plot(x[0], x[1])
plot(x[0,0], x[1,0], 'go')
plot(x[0,-1], x[1,-1], 'ro')

# More plot decorations.
title('2D Brownian Motion')
xlabel('x')
ylabel('y')
axis('equal')
show()
