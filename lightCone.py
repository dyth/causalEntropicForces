#!/usr/bin/env python
"""create light cone from all possible moves"""
import matplotlib.pyplot as plt
import random

from noughtsCrosses import *


def randomCoordinates():
    'return 2-tuple of random numbers between 0 and 2'
    x = random.randint(0, 2)
    y = random.randint(0, 2)
    return x, y


def randomMove(player, board):
    'randomly select move of player'
    x, y = randomCoordinates()
    newBoard = move(player, board, x, y)
    if (newBoard != None):
        return newBoard, 3*x + y
    else:
        return randomMove(player, board)


def randomWalk(board, player, history):
    'take a random walk through the board'
    winner = evaluate(board)
    if (winner != None or len(history) == 9):
        return history, winner
    else:
        board, move = randomMove(player, board)
        history.append(move)
        return randomWalk(board, nextPlayer(player), history)

    

print "matplotlib finished building"
ax = plt.gca()
plt.ion()
plt.show()
while True:
    history, winner = randomWalk(initialBoard, 1, [])
    colour = 'g' if (winner == 1) else 'r'
    ax.plot(history, color=colour)
    plt.draw()
    raw_input()
