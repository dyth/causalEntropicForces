#!/usr/bin/env python
"""output a 2D and 3D plot of the monte carlo path sampling"""
from json import load
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.stats import gaussian_kde
from numpy import array
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import proj3d


class Arrow3D(FancyArrowPatch):
    def __init__(self, xs, ys, zs, *args, **kwargs):
        FancyArrowPatch.__init__(self, (0,0), (0,0), *args, **kwargs)
        self._verts3d = xs, ys, zs

    def draw(self, renderer):
        xs3d, ys3d, zs3d = self._verts3d
        xs, ys, zs = proj3d.proj_transform(xs3d, ys3d, zs3d, renderer.M)
        self.set_positions((xs[0],ys[0]),(xs[1],ys[1]))
        FancyArrowPatch.draw(self, renderer)


def log_volume_fractions(walks):
    'return log_volume_fractions on a set of random walks'
    points = array([w[-1] for w in walks])
    kernel = gaussian_kde(points.T)
    return [kernel.pdf(w[-1]) for w in walks], kernel


def causal(cur_macrostate, num_sample_paths, environment):
    'calculate the path integral'
    # Monte Carlo path sampling
    walks, sample_paths, initial_forces = [], [], []
    for _ in range(num_sample_paths):
        walk, forces = [cur_macrostate], []
        count = int(environment.TAU / environment.TIMESTEP)
        # explore the random walk until 
        while count != 0:
            u, f = environment.step_microstate(walk[-1])
            # if valid then redo
            if environment.valid(walk, u):
                walk.append(u)
                forces.append(f)
                count -= 1
        sample_paths.append(walk[1:])
        initial_forces.append(forces[0])
        walks.append(walk)
    # Kernel Density Estimation of log volume fractions
    log_volume_fracs, kernel = log_volume_fractions(sample_paths)
    # sum force contributions
    force = sum([f*log_volume_fracs[i] for i, f in enumerate(initial_forces)])
    force = 2.0 * environment.TC * force / (environment.TR * num_sample_paths)
    return walks, force, kernel


def plot_2D(walks, environment, cur_macrostate, difference):
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
        ax.plot(walk_plot[0][:50], walk_plot[1][:50], zorder=0)
    ax.arrow(cur_macrostate[0], cur_macrostate[1], difference[0], difference[1], width=3.0, head_width=9.0, shape='full', facecolor='black', zorder=10)
    plt.show()
    fig.savefig('images/particleBoxLightCone2D.png', dpi=300)


def plot_3D(walks, environment, cur_macrostate, difference):
    '2D plot of paths'
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d', aspect = 'equal')
    ax.set_title("Particle in a 2 dimensional box")
    ax.set_xlim(0.0, 400.0)
    ax.set_ylim(-160.0, 240.0)
    ax.set_zlim(0.0, 50.0)
    ax.set_xlabel("Position / metres")
    ax.set_ylabel("Position / metres")
    ax.set_zlabel("Time / ms")
    for walk in walks:
        walk_plot = [[w[i] for w in walk] for i in range(environment.DIMS)]
        ax.plot(walk_plot[0][:10], walk_plot[1][:10], 5.0*array(range(len(walk_plot[0][:10]))))
    arrow_prop_dict = dict(linewidth=3.0, mutation_scale=1.0, arrowstyle='-|>', color='k', shrinkA=0, shrinkB=0)
    a = Arrow3D([cur_macrostate[0], cur_macrostate[0] + difference[0]], [cur_macrostate[1], cur_macrostate[1] + difference[1]], [0.0, 0.0], **arrow_prop_dict)
    ax.add_artist(a)
    plt.show()
    fig.savefig('images/particleBoxLightCone.png', dpi=300)
    

def plot_kernel(kernel, cur_macrostate, difference):
    xmin, xmax = 0, 400
    ymin, ymax = 0, 80

    # Peform the kernel density estimate
    xx, yy = np.mgrid[xmin:xmax:100j, ymin:ymax:100j]
    positions = np.vstack([xx.ravel(), yy.ravel()])
    f = np.reshape(kernel(positions).T, xx.shape)

    fig = plt.figure()
    ax = fig.add_subplot(111, aspect = 'equal')
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
    ax.set_xlabel('Position / metres')
    ax.set_ylabel('Position / metres')
    ax.set_title("Particle in a 2 dimensional box")
    ax.arrow(cur_macrostate[0], cur_macrostate[1], difference[0], difference[1], width=3.0, head_width=9.0, shape='full', facecolor='black')
    plt.show()
    fig.savefig('images/density.png', dpi=300)

    
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
    walks, force, kernel = causal(cur_macrostate, num_sample_paths, environment)
    difference = environment.step_macrostate(array([0.0, 0.0]), force)
    plot_kernel(kernel, cur_macrostate, difference)
    plot_3D(walks, environment, cur_macrostate, difference)
    plot_2D(walks, environment, cur_macrostate, difference)
    
    
