#!/usr/bin/env python
"""perform kernel density estimation on each dimension, then get result"""
import numpy as np
from fastkde import fastKDE

    
def kde(*walks):
    'use fastKDE to perform kernel density estimation, return logProbs'
    myPDF, _ = fastKDE.pdf(*walks)
    return [myPDF[[[w[i]] for w in walks]][0] for i in range(len(walks[0]))]

# Generate 100000 datapoints in three different lists representing dimensions
N = 100000
var1 = 10 + 50 * np.random.normal(size=N)
var2 = 10 + 50 * np.random.normal(size=N)
var3 = 10 + 50 * np.random.normal(size=N)

lists = kde(var1, var2, var3)
print lists[765]
