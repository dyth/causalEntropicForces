# Causal Entropic Forces

Reimplementation of [Causal Entropic Forces](http://math.mit.edu/~freer/papers/PhysRevLett_110-168702.pdf), bolstered by pseudocode and equations in [supplementary material](https://journals.aps.org/prl/supplemental/10.1103/PhysRevLett.110.168702).

The algorithm is able to find policies unsupervised from an environment, provided it can interact with the environment beforehand. To do this, it iteratively finds the next best move it can take, represented in the below diagrams by the thick black arrow.

First, it generates random walks throughout the environment to sample the evolution of the environment and agent.
![lightCone2D](https://raw.githubusercontent.com/dyth/causalEntropicForces/secondImplementation/images/particleBoxLightCone2D.png)

For each destination the random walks end, the algorithm computes the likelihood (conditional probability density) that the system will evolve to that particular destination. Then, a weighted average of all first steps are taken with this likelihood to find the step that maximises the number of potential futures.
![path](https://raw.githubusercontent.com/dyth/causalEntropicForces/secondImplementation/images/density.png)

The first 50 steps are here expressed as a light cone.
![paths](https://raw.githubusercontent.com/dyth/causalEntropicForces/secondImplementation/images/particleBoxLightCone.png)

## Prerequisites

Python libraries: `numpy`, `matplotlib`, `scipy`

```
$ pip install numpy matplotlib scipy
```

## Run current version

Properties of the agent can be specified in `config.json`.

```
{
	"environment"      : "<name_of_python_file_with_environment_class>",
	"num_sample_paths" : 200, // number of paths to sample
	"plot"             : {true, false},
	"steps"            : 100, // number of steps within the policy
	"cur_macrostate"   : null // for use in plotting light cones
}
```

To design your own environment, ensure that it contains the same methods and variables as those in `particleBox.py`. The agent can then be run by the following command.

```
$ python agent.py
```

## History
For more code and other derivative agents, download the v0.5 release
