#!/usr/bin/env python
"""
Adapted from https://stackoverflow.com/questions/18988855/fitting-maxwell-boltzman-distribution-in-python
"""
import scipy.stats as stats
import matplotlib.pyplot as plt
import numpy as np

maxwell = stats.maxwell
data = maxwell.rvs(loc=0, scale=5, size=10000)

params = maxwell.fit(data, floc=0)
print(params)
# (0, 4.9808603062591041)

plt.hist(data, bins=20, normed=True)
x = np.linspace(0, 25, 100)
plt.plot(x, maxwell.pdf(x, *params), lw=3)
plt.show()
