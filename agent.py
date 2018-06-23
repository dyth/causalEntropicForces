#!/usr/bin/env python
"""Model Based Reflex Agent with Entropic Forcing"""
from particleBox import particleBox
from sys import exit
from numpy import array, append as numpy_append
from scipy.stats import gaussian_kde
from json import load
from math import exp


def log_volume_fractions(walks):
    'return log_volume_fractions on a set of random walks'
    points = []
    for i in range(len(walks)):
        for j in range(len(walks[i])-1):
            doublePoint = numpy_append(walks[i][j], walks[i][j+1])
            walks[i][j] = doublePoint
            points.append(doublePoint)
        walks[i] = walks[i][:-1]
    points = array(points)
    kernel = gaussian_kde(points.T)
    logpdfs = [sum(kernel.logpdf(array(w).T)) for w in walks]
    #logpdfs = [exp(l) for l in logpdfs]
    minimum = min(logpdfs)
    logpdfs = [exp(minimum - l) for l in logpdfs]
    total = sum(logpdfs)
    logpdfs = [l / total for l in logpdfs]


    # now plot x and y transition kernels

    
    
    print logpdfs
    return logpdfs

    
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
    force = sum([f*log_volume_fracs[i] for i, f in enumerate(initial_forces)])
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
