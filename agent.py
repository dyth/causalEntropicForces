#!/usr/bin/env python
"""Model Based Reflex Agent with Entropic Forcing"""
from particleBox import particleBox
from sys import exit
from numpy import array, append as numpy_append
from scipy.stats import gaussian_kde
from json import load
from math import exp, atan, sqrt

import numpy as np
from matplotlib import pyplot as plt


def log_volume_fractions2(walks):
    'return log_volume_fractions on a set of random walks'
    endpoints = array([walk[-1] for walk in walks])
    #print endpoints
    length = len(walks[0]) / 2
    points = array([walk[length:] for walk in walks]).reshape((-1,2))
    kernel = gaussian_kde(points.T)
    
    """
    fig = plt.figure()
    ax = fig.add_subplot(111, aspect = 'equal')
    xx, yy = np.mgrid[0:400:200j, 0:80:200j]
    f = np.reshape(kernel(np.vstack([xx.ravel(), yy.ravel()])).T, xx.shape)
    ax.set_xlim(0, 400)
    ax.set_ylim(0, 80)
    ax.imshow(np.rot90(f), cmap='Blues', extent=[0, 400, 0, 80])
    plt.show()
    plt.pause(0.001)
    input()
    """
    
    logpdfs = -array([kernel.pdf(endpoints.T)]).T
    return logpdfs


def log_volume_fractions_3d(walks):
    'compute log_volume_fractions in 3D'
    walks = array([[list(w) + [i] for i, w in enumerate(ws)] for ws in walks])
    kernel = gaussian_kde(walks.reshape((-1, 3)).T)
    length = len(walks[0]) / 2
    logpdfs = -array([kernel.pdf(w[length:].T) for w in walks]).sum(axis=1)
    return logpdfs


def log_volume_fractions_slice(walks):
    'compute log_volume_fractions using timeslices'
    kernels = []
    for i in range(len(walks[0])):
        points = array([walk[i] for walk in walks]).reshape((-1,2))
        kernels.append(gaussian_kde(points.T))
    f = [sum([kernels[i].pdf(w)[0] for i, w in enumerate(ws)]) for ws in walks]
    return f


def log_volume_fractions(walks):
    'compute log_volume_fractions using timeslices'
    kernels = []
    for i in range(len(walks[0])):
        points = array([walk[i] for walk in walks]).reshape((-1,2))
        kernels.append(gaussian_kde(points.T))
    #f = [sum([kernels[i].pdf(w)[0] for i, w in enumerate(ws)]) for ws in walks]
    f = [sum([k.pdf(ws[0])[0] for k in kernels]) for ws in walks]
    return f


def log_volume_fractions(walks):
    'compute log_volume_fractions using transition kernel'
    points = []
    transitions = []
    for walk in walks:
        transition = []
        for i, w in enumerate(walk[:-1]):
            point = list(w) + list(walk[i+1])
            transition.append(point)
            points.append(point)
        transitions.append(transition)
    k = gaussian_kde(array(points).T)
    probs = array([sum([k.pdf(t) for t in ts]) for ts in transitions])
    probs = probs / np.sqrt((np.sum(probs**2)))
    return probs

    
def calculate_causal_entropic_force(cur_macrostate, num_sample_paths, environment):
    'calculate the path integral'
    # Monte Carlo path sampling
    sample_paths, initial_forces = [], []
    for _ in range(num_sample_paths):
        walk = [cur_macrostate]
        forces = [array([0.0 for _ in range(environment.DIMS)])]
        count = int(environment.TAU / environment.TIMESTEP)
        # explore the random walk until 
        while count != 0:
            u, f = environment.step_microstate(walk[-1], forces[-1])
            # if valid then redo
            if environment.valid(walk, u):
                walk.append(u)
                forces.append(f)
                count -= 1
        sample_paths.append(walk[1:])
        initial_forces.append(forces[1])
    # Kernel Density Estimation of log volume fractions
    log_volume_fracs = log_volume_fractions(sample_paths)
    # sum force contributions
    force = sum([f*l for i, l in zip(initial_forces, log_volume_fracs)])
    return 2.0 * environment.TC * force / (environment.TR * num_sample_paths)


def perform_causal_entropic_forcing(num_sample_paths, steps, plot, environment):
    'reflex loop of model-based reflex agent'
    cur_macrostate = environment.start
    path = [cur_macrostate]
    print cur_macrostate
    for _ in range(steps):
        # move agent
        causal_entropic_force = calculate_causal_entropic_force(cur_macrostate, num_sample_paths, environment)
        cur_macrostate = environment.step_macrostate(cur_macrostate, causal_entropic_force)
        # keep track of motion
        if not environment.valid(path, cur_macrostate):
            print "Error: Agent in invalid environment state,", cur_macrostate
            exit()
        print cur_macrostate
        path.append(cur_macrostate)
        # plot if true
        if plot == True:
            environment.update_plot(path)


if __name__ == "__main__":
    # open config.json
    with open('config.json') as configFile:
        config = load(configFile)

    # import environment
    name = config["environment"]
    environment_name = getattr(__import__(name, fromlist=[name]), name)
    environment = environment_name()

    # determine features of agent
    num_sample_paths = config["num_sample_paths"]
    steps = config["steps"]
    plot = config["plot"]
    if plot == True:
        environment.plot()

    # loop forever
    perform_causal_entropic_forcing(num_sample_paths, steps, plot, environment)
