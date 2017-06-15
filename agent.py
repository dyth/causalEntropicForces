#!/usr/bin/env python
"""perform kernel density estimation on 2D grid"""
from particleBox import *
from monteCarloPathSampling import *
from kde import *


def average(logProb, points, position):
    'take weighted average of logProb and points offset to find mean outcome'
    mean = [0.0, 0.0]
    points = [point - position for point in points]
    for index in range(len(points)):
        mean += logProb[index] * points[index]
    return [m / float(len(points)) for m in mean]
    

def steps(position, bounds, number):
    'calculate where the next step should be'
    points = monteCarloPathSampling(start, 100, depth, dims, stepSize, valid)
    points = array(points)
    logProb, allPoints = estimate(points, bounds, number)
    mean = average(logProb, allPoints, position)
    magnitude = sum([m**2 for m in mean])
    move = [-stepSize * m / magnitude for m in mean]
    return move


def forcing(position, bounds, steps, dims):
    'move particle according to force for steps'
    number = [b[1] - b[0] for b in bounds]
    history = []
    for _ in range(steps):
        move = steps(position, bounds, number)
        position = [position[i] + move[i] for i in range(dims)]
        history.append(position)
    return history

        
#forcing(start, bounds, 100, dims)
number = [b[1] - b[0] for b in bounds]
print steps(start, bounds, number)
