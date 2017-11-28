#!/usr/bin/env python
"""Model Based Reflex Agent with Entropic Forcing"""
from particleBox import ParticleBox
from sys import exit
from numpy import array
from scipy.stats import gaussian_kde


def log_volume_fractions(walks):
    'return log_volume_fractions on a set of random walks'
    points = array([w[-1] for w in walks])
    kernel = gaussian_kde(points.T)
    return [-kernel.logpdf(w[-1]) for w in walks]

    
def calculate_causal_entropic_force(cur_macrostate, num_sample_paths, environment):
    'calculate the path integral'
    # Monte Carlo path sampling
    sample_paths, initial_forces = [], []
    for _ in range(num_sample_paths):
        walk, force = [cur_macrostate], None
        count = int(environment.TAU / environment.TIMESTEP)
        # explore the random walk until
        while count != 0:
            u, f = environment.step_microstate(walk[-1])
            # if valid then redo
            if environment.valid(walk, u):
                walk.append(u)
                count -= 1
                # only the initial force is needed
                if force == None:
                    force = f
        sample_paths.append(walk[1:])
        initial_forces.append(force)
    # Kernel Density Estimation of log volume fractions
    log_volume_fracs = log_volume_fractions(sample_paths)
    # sum force contributions
    force = sum([f*log_volume_fracs[i] for i, f in enumerate(initial_forces)])
    return 2.0 * environment.TC * force / (environment.TR * num_sample_paths)


def perform_causal_entropic_forcing(environment):
    'reflex loop of model-based reflex agent'
    cur_macrostate = environment.start
    print cur_macrostate
    while True:
        # move agent
        causal_entropic_force = calculate_causal_entropic_force(cur_macrostate, num_sample_paths, environment)
        cur_macrostate = environment.step_macrostate(cur_macrostate, causal_entropic_force)
        # keep track of motion
        if not environment.valid(path, cur_macrostate):
            print "Error: Agent in invalid environment state,", cur_macrostate
            exit()
        print cur_macrostate
        path.append(cur_macrostate)

        
path, num_sample_paths = [], 500
environment = ParticleBox()
perform_causal_entropic_forcing(environment)
