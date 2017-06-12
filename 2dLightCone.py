#!/usr/bin/env python
"""create light cone frrahom all possible moves"""
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import random
import math

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
        return newBoard, x, y
    else:
        return randomMove(player, board)


def randomWalk(board, player, xs, ys):
    'take a random walk through the board'
    winner = evaluate(board)
    if (winner != None or len(xs) == len(board)):
        return xs, ys, winner
    else:
        board, x, y = randomMove(player, board)
        xs.append(x)
        ys.append(y)
        return randomWalk(board, nextPlayer(player), xs, ys)


def historyToEncoding(light, history, i):
    'convert a history list of moves into light cone representation'
    if (len(light) == len(history)):
        return light
    else:
        light.append(float(light[-1]) + float(history[i])/(3 ** i))
        return historyToEncoding(light, history, i+1)

    
def enum(l):
    'return enumerated list of 0 to len(l)'
    return range(len(l))


def centreLight(light):
    'centre the light cone around 0'
    light = [light[i] + 1.0 / (2.0 * (3 ** i)) for i in enum(light)]
    return light



print "matplotlib finished building"
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_title("Game Tree expressed as a light cone")
#ax.axes.get_xaxis().set_visible(False)
ax.set_ylabel("Move No.")
plt.ion()
plt.show()
while True:
    xs, ys, winner = randomWalk(initialBoard, 1, [0], [0])
    xs = historyToEncoding([0], xs, 1)
    ys = historyToEncoding([0], ys, 1)
    xs = centreLight(xs)
    ys = centreLight(ys)
    colour = 'g' if (winner == 1) else 'r'
    ax.plot(xs, ys, enum(xs), color=colour)
    plt.draw()
    plt.pause(0.05)
