# Historical Files

Contains files (and documentation) no longer relevant to the current implementation. As this has been moved to the history subdirectory, a `..` may need to be added to paths when importing an environment.

Code is based on the algorithm described [this paper](http://math.mit.edu/~freer/papers/PhysRevLett_110-168702.pdf). The underlying idea is substantiated with pseudocode examples in the [supplementary material](https://journals.aps.org/prl/supplemental/10.1103/PhysRevLett.110.168702), which form the basis of this repository.

## Prerequisites

Python libraries: `numpy`, `matplotlib`, `scipy`

## Agent

`agent` contains an implementation of the described algorithm in the paper.

### Approximations

The directory `agentApproximations` contains an approximation of the algorithm described in the above paper which optimises computation speed at the expense of accuracy in physical units.

There are three stages in the agent and are found in `monteCarloPathSampling.py`, `agent.py` and `kde.py`. To run the agent with the Particle in a Box example, do `$ python agent.py`. First, `agent.py` calls `monteCarloPathSampling.py`, which stochastically calculates many random walks which are then used to estimate the density of the state space in `kde.py`, which uses the scikit-learn implementation of kernel density estimation. The sum over all possible moves is weighted with the log-likelihood of the KDE estimated probability to find the most probable direction that a randomised process would end up. A step in the opposite direction is thus taken.

`agentEM.py` and `kdeEM.py` combine an agent with an expectation-maximsation algorithm, such that the agent now advances to the sample mean of the stochastic walks obtained from kernel density estimation. `agentEMWLLN.py` achieves this at a faster rate using the weak law of large numbers to advance the particle to the statistical mean of the endpoints of each random walk.

`config.json` stores agent specific properties, whereas each environment python file contains state variables.

## Particle in a Box

A recommended config file is:

{
	"game"    : "particleBox",
	"style"   : "max",
	"samples" : "400",
	"steps"   : "10",
	"dist"    : "Gaussian"
}

The directory contains `particleBox.py`, a configuration file with information about the simulation. It has a start state, a boundary and a `valid` function to determine if the next move is valid or not.

Running `particleBoxAgentPlot.py` produces the following graphs animated with real-time updates for every step.

![path](https://raw.githubusercontent.com/dyth/causalEntropicForces/master/images/path.png)
![2DPaths](https://raw.githubusercontent.com/dyth/causalEntropicForces/master/images/2DPaths.png)
![2DPoints](https://raw.githubusercontent.com/dyth/causalEntropicForces/master/images/2DPoints.png)
![2DPointsKDE](https://raw.githubusercontent.com/dyth/causalEntropicForces/master/images/2DPointsKDE.png)
![2DCone](https://raw.githubusercontent.com/dyth/causalEntropicForces/master/images/2DCone.png)

## Noughts and Crosses

Noughts and Crosses was chosen because it was simple enough to implement, yet orthogonal to the other examples in the supplementary material because it has a well-defined goal state.

`noughtsCrosses.py` is a rule configuration file for the game of noughts and crosses: starting state; next player; rule for nextmove; evaluation function for board.

`lightCone.py` plots a 2 dimensional light cone graph generated from many random walks of a game using `pyplot` from `matplotlib`. On the Y-axis is the number of moves from the start.

<img src="https://latex.codecogs.com/gif.latex?\begin{array}{ccc}&space;0&space;&&space;1&space;&&space;2&space;\\&space;3&space;&&space;4&space;&&space;5&space;\\&space;6&space;&&space;7&space;&&space;8&space;\\&space;\end{array}" title="\begin{array}{ccc} 0 & 1 & 2 \\ 3 & 4 & 5 \\ 6 & 7 & 8 \\ \end{array}" />

Using the above enumeration of a noughts and crosses board, a move is represented in a tree with a move on square i on the ith branch on the tree. All the paths start at a node representing the initially empty board.

![NoughtsCrossesCone](https://raw.githubusercontent.com/dyth/causalEntropicForces/master/images/noughtsCrosses.png)

Green lines indicate random walks representing games which the first player wins. Red lines indicate otherwise.

`2dlightCone.py` plots a light cone graph in 3 dimensions, using cartesian coordinates to represent a move on the board instead of enumerating the board as in `lightCone.py`. They produce the following graphs respectively.

![2DNoughtsCrossesCone](https://raw.githubusercontent.com/dyth/causalEntropicForces/master/images/noughtsCrosses2D.png)
