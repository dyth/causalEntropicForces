# Causal Entropic Forces

Code is based on the algorithm described [this paper](http://math.mit.edu/~freer/papers/PhysRevLett_110-168702.pdf). The underlying idea is substantiated with pseudocode examples in the [supplementary material](https://journals.aps.org/prl/supplemental/10.1103/PhysRevLett.110.168702), which form the basis of this repository.

Noughts and Crosses was chosen because it was simple enough to implement, yet orthogonal to the other examples in the supplementary material because it has a well-defined goal state.

`lightCone.py` plots a light cone graph generated from many random walks of a game using `pyplot` from `matplotlib`. On the Y-axis is the number of moves from the start.

<img src="https://latex.codecogs.com/gif.latex?$$&space;\begin{array}{ccc}&space;1&space;&&space;2&space;&&space;3&space;\\&space;4&space;&&space;5&space;&&space;6&space;\\&space;7&space;&&space;8&space;&&space;9&space;\\&space;\end{array}&space;$$" title="$$ \begin{array}{ccc} 1 & 2 & 3 \\ 4 & 5 & 6 \\ 7 & 8 & 9 \\ \end{array} $$"/>

Using the above enumeration of a noughts and crosses board, a move is represented in a tree with a move on square i on the ith branch on the tree. All the paths start at a node representing the initially empty board.

Green lines indicate random walks representing games which the first player wins. Red lines indicate otherwise.

`noughtsCrosses.py` contain the rules for the game of noughts and crosses: starting state; next player; rule for nextmove; evaluation function for board.
