#!/usr/bin/env python
"""
RandomBot -- A simple strategy: enumerates all legal moves, and picks one 
uniformly at random.

We've implemented this a little inefficiently, so you can see what the legal 
moves are, and how to enumerate all of them.

"""

# Import the API objects
from api import *

import random


def get_move(state, id):
    """
    Function that gets called every turn. This is where to implement the strategies.
    
    Be sure to make a legal move. Illegal moves, like giving a source planet you
    don't own, will lose you the game.
    
    If you return a source and destination, 50% of the ships of the source 
    planet (rounded down) will be sent to the destination. If that planet is 
    owned by the enemy or neutral when they arrive, they will attack it, if it is
    owned by you, they will reinforce it (add to the number of ships stationed).

    :param State state: An object representing the gamestate. This includes a link to the 
        map, ownership of each planet, and fleets currently in transit.
    :param int id: Which player you are: 1 or 2.
        
    :return: None, indicating no move is made, or a pair of integers, 
        indicating a move; the first indicates the source planet, the second the 
        destination.  
    """

    # get the planets
    mine = state.planets(id)
    all = state.planets()
    
    # Generate all possible pairs with the first element from mine
    # and the second from all. 
    moves = [(m,a) for m in mine for a in all]

    # NB: This is a neat, but slightly advanced python trick called a 
    # "list comprehension:. See http://www.learnpython.org/en/List_Comprehensions
    # We could also have used two nested loops:
    #
    # moves = []
    # for m in mine:
    #   for a in all:
    #     moves.append((m,a))

    # None is also a legal move
    moves.append(None)

    # Return a random choice 
    return random.choice(moves) 
