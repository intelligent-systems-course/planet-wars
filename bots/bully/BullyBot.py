#!/usr/bin/env python
"""
BullyBot - A simple strategy: always  attacks the weakest planet with its 
strongest.  
"""

# Import the API objects
from api import *

def get_move(state):
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
        
    :return: None, indicating no move is made, or a pair of integers, 
        indicating a move; the first indicates the source planet, the second the 
        destination.  
    """

    source = None
    dest = None

    source_strength = -1        # source score must be as large as possible (start with very low score)
    dest_strength = sys.maxsize # destination score must be as little as possible (start with high score)

    # Find my strongest planet (largest number of stationed ships)
    for mine in state.planets(id):
        if mine.number_ships() > source_score:
            source_score = mine.number_ships()
            source = mine

    # Find the weakest enemy or neutral planet (lowest amount of ships).
    for his in pw.planets(util.other(id)):
        if his.number_ships() < dest_score:
            dest_score = his.number_ships()
            dest = his
            
    if source is None or dest is None:
        return None
        
    return (source.id(), dest.id())

