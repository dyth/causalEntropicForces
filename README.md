# Causal Entropic Forces

Code is based on the algorithm described [this paper](http://math.mit.edu/~freer/papers/PhysRevLett_110-168702.pdf). The underlying idea is substantiated with pseudocode examples in the [supplementary material](https://journals.aps.org/prl/supplemental/10.1103/PhysRevLett.110.168702), which form the basis of this repository.

Noughts and Crosses was chosen because it was simple enough to implement, yet orthogonal to the other examples in the supplementary material because it has a well-defined goal state.

`lightCone.py` plots random walks of a game. It utilises `pyplot` from `matplotlib`.

`noughtsCrosses.py` contain the rules for the game of noughts and crosses: starting state; next player; rule for nextmove; evaluation function for board.
