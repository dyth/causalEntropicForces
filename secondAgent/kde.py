#!/usr/bin/env python
"""perform kernel density estimation on each dimension, then get result
import warnings
import numpy as np
from sklearn.neighbors import KernelDensity


def kde(x):
    'use scikit-learn to perform kernel density estimation, return logProbs'
    warnings.filterwarnings("ignore")
    kde = KernelDensity(bandwidth=0.2, kernel='gaussian')
    kde.fit(x)
    return kde.score_samples(x)
"""

import numpy as np
from fastkde import fastKDE

# Generate 100000 datapoints in three different lists representing dimensions
N = 1000000
var1 = np.random.normal(size=N)
var2 = np.random.normal(size=N)
var3 = np.random.normal(size=N)

#Do the self-consistent density estimate
myPDF, _ = fastKDE.pdf(var1 ,var2, var3)
print myPDF.shape
