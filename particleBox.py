#!/usr/bin/env python
"""particle in a box which drifts towards the centre"""
from numpy import array

# state variables
start = [-50.0, 0.0]
bounds = ((-100.0, 200.0), (-100.0, 100.0))
dims = len(bounds)


def valid(walk, p):
    'determine whether a walk is valid'
    if ((p[0] < bounds[0][0]) or (p[0] > bounds[0][1]) or
        (p[1] < bounds[1][0]) or (p[1] > bounds[1][1])):
        return False
    else:
        return True
