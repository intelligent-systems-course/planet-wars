#!/usr/bin/env python
"""
EmptyBot - a skeleton of a bot that you can modify. Copy this file to something 
like MyBot.py and fill in the blanks.

Every bot contains just a single function: it receives the game state as a 
parameter, and return a move. The 

"""

# Import the API objects
from api import *


def get_move(state, id):
    """
    Function that gets called every turn. This is where to implement the strategies.
    
    Be sure to make a legal move. Illegal moves, like giving a source planet you
    don't own will lose you the game.
    
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

    # The source variable will contain the planet from which we send the ships.
    # Create a source planet, if you want to know what this object does, then read the API
    source = None

    # The dest variable will contain the destination, the planet to which we send the ships.
    destination = None

    # (1) Implement an algorithm to determine the source planet to send your ships from    
    # for a simple working example, try
    # source = state.my_planets()[0]

    # (2) Implement an algorithm to determine the destination planet to send your ships to    
    # for a simple working example try
    # destination = state.his_planets()[0]

    return (source, destination) # to do nothing, return None
