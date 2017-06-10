#!/usr/bin/env python
"""create light cone from all possible moves"""
import matplotlib.pyplot as plt
import random


def randomCoordinates():
    'return 2-tuple of random numbers between 0 and 2'
    x = random.randint(0, 3)
    y = random.randint(0, 3)
    return x, y


def randomMove(player, board):
    'randomly select move of player'
    x, y = randomCoordinates()
    newBoard = move(player, board, x, y)
    if (newBoard == None):
        return randomMove(player, board)
