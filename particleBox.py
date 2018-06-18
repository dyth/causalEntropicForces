#!/usr/bin/env python
"""particle in a box which drifts towards the centre"""
from numpy import array
from scipy.constants import Boltzmann
from scipy.stats import norm
from math import sqrt, log
from matplotlib import pyplot as plt

class particleBox:

    def __init__(self):
        # state variables
        self.length = 400.0
        self.start = array([self.length/10.0, self.length/10.0])
        self.bounds = ((0.0, self.length), (0.0, self.length/5.0))
        self.DIMS = len(self.bounds)

        self.KB = Boltzmann      # Boltzmann Constant
        self.TAU = 10.0          # Time horizon
        self.TR = 400000.0       # Temperature of random movement
        self.TC = 5.0 * self.TR  # Causal Path Temperature
        self.TIMESTEP = 0.025    # Interval between random walk sampling
        self.MASS = 10.0 ** -21

        self.MEAN = 0.0
        self.AMPLITUDE = sqrt(self.MASS * self.KB * self.TR) / self.TIMESTEP
        self.DISTRIBUTION = norm(0.0, 1.0)


    def step_microstate(self, cur_state, previousForce):
        'compute next distance by Forward Euler'
        random = self.DISTRIBUTION.rvs(self.DIMS)
        force = self.AMPLITUDE * random + self.MEAN
        euler = self.TIMESTEP / (2.0*self.MASS)
        pos = cur_state + (previousForce + force) * euler
        return pos, force
    

    def valid(self, walk, position):
        'determine whether a walk is valid'
        if ((position[0] < self.bounds[0][0]) or
            (position[0] > self.bounds[0][1]) or
            (position[1] < self.bounds[1][0]) or
            (position[1] > self.bounds[1][1])):
            return False
        else:
            return True

    
    def step_macrostate(self, cur_macrostate, causal_entropic_force):
        'move the particle subject to causal_entropic_force'
        euler = self.TIMESTEP / (2.0*self.MASS)
        return cur_macrostate + causal_entropic_force * euler

    
    def plot(self):
        'initialise an interactive plot'
        plt.gca(aspect = 'equal')
        plt.title("Particle in a 2 dimensional box")
        plt.xlim(self.bounds[0][0], self.bounds[0][1])
        plt.ylim(self.bounds[1][0], self.bounds[1][1])
        plt.ion()
        plt.show()
        plt.pause(0.001)
        self.hl, = plt.plot([], [], linewidth=0.25, color='k')

        
    def update_plot(self, path):
        'plot the path of the particle on a pyplot graph'
        path = [[p[i] for p in path] for i in range(self.DIMS)]
        self.hl.set_xdata(path[0])
        self.hl.set_ydata(path[1])
        plt.draw()
        plt.pause(0.0001)
