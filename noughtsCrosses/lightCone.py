#!/usr/bin/env python
"""create light cone from all possible moves"""
import matplotlib.pyplot as plt
import random
import math

from noughtsCrosses import *

# state variables
number, im = 100, True


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
    if (winner != None or len(history) == len(board)):
        return history, winner
    else:
        board, move = randomMove(player, board)
        history.append(move)
        return randomWalk(board, nextPlayer(player), history)


def historyToEncoding(light, history, i):
    'convert a history list of moves into light cone representation'
    if (len(light) == len(history)):
        return light
    else:
        light.append(float(light[-1]) + float(history[i])/(9 ** i))
        return historyToEncoding(light, history, i+1)

    
def enum(l):
    'return enumerated list of 0 to len(l)'
    return range(len(l))


def centreLight(light):
    'centre the light cone around 0'
    light = [light[i] + 1.0 / (2.0 * (9 ** i)) for i in enum(light)]
    return light



print "matplotlib finished building"
ax = plt.gca()
ax.set_title("Game Tree expressed as a light cone")
ax.axes.get_xaxis().set_visible(False)
ax.set_ylabel("Move No.")
plt.ion()
plt.show()
for _ in range(number):
    history, winner = randomWalk(initialBoard, 1, [0])
    light = historyToEncoding([0], history, 1)
    light = centreLight(light)
    colour = 'g' if (winner == 1) else 'r'
    ax.plot(light, enum(light), color=colour)
    plt.draw()
    plt.pause(0.01)

if im:
    plt.savefig('../images/noughtsCrosses.png', dpi=900)
