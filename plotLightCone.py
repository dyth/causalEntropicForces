#!/usr/bin/env python
"""output a 2D and 3D plot of the monte carlo path sampling"""
from agent import log_volume_fractions
from json import load
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from numpy import array


def get_walks_and_force(cur_macrostate, num_sample_paths, environment):
    'calculate the path integral'
    # Monte Carlo path sampling
    walks, sample_paths, initial_forces = [], [], []
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
        walks.append(walk)
        sample_paths.append(walk[1:])
        initial_forces.append(force)
    # Kernel Density Estimation of log volume fractions
    log_volume_fracs = log_volume_fractions(sample_paths)
    # sum force contributions
    force = sum([f*log_volume_fracs[i] for i, f in enumerate(initial_forces)])
    force = 2.0 * environment.TC * force / (environment.TR * num_sample_paths)
    return walks, force


def plot_2D(walks, environment):
    '2D plot of paths'
    fig = plt.figure()
    ax = fig.add_subplot(111, aspect = 'equal')
    ax.set_title("Particle in a 2 dimensional box")
    ax.set_xlim(environment.bounds[0][0], environment.bounds[0][1])
    ax.set_ylim(environment.bounds[1][0], environment.bounds[1][1])
    ax.set_xlabel("Position / metres")
    ax.set_ylabel("Position / metres")
    for walk in walks:
        walk_plot = [[w[i] for w in walk] for i in range(environment.DIMS)]
        ax.plot(walk_plot[0], walk_plot[1])
    plt.show()
    fig.savefig('images/particleBoxLightCone2D.png', dpi=300)


def plot_3D(walks, environment):
    '2D plot of paths'
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d', aspect = 'equal')
    ax.set_title("Particle in a 2 dimensional box")
    ax.set_xlim(0.0, 500.0)
    ax.set_ylim(-250.0, 250.0)
    ax.set_zlim(0.0, 1000.0)
    ax.set_xlabel("Position / metres")
    ax.set_ylabel("Position / metres")
    ax.set_zlabel("Time / ms")
    for walk in walks:
        walk_plot = [[w[i] for w in walk] for i in range(environment.DIMS)]
        ax.plot(walk_plot[0], walk_plot[1], 5.0*array(range(len(walk_plot[0]))))
    plt.show()
    fig.savefig('images/particleBoxLightCone.png', dpi=300)
    
    
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
    cur_macrostate = config["cur_macrostate"]
    if cur_macrostate == None:
        cur_macrostate = environment.start
    
    # calculate the force and walks in cur_macrostate to plot graphs
    walks, force = get_walks_and_force(cur_macrostate, num_sample_paths, environment)
    #plot_3D(walks, environment)
    #plot_2D(walks, environment)
