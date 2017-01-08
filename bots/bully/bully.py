#!/usr/bin/env python
"""
BullyBot - A simple strategy: ...

It also has a parameter: with probability 'nomove' it chooses not to make a move.
"""

# Import the API objects

import api.util as u
from api import State
import random, sys

class Bot:

    def __init__(self):
        pass

    def get_move(self, state):

        # Find out which player we are
        my_id = state.whose_turn()

        # Our move: these will contain Planet objects
        source = None
        dest = None

        source_strength = -1         # source score must end up as large as possible (start with very low value)
        dest_strength = float('inf') # destination score must end up as small as possible (start with high value)

        # Find my strongest planet (largest number of stationed ships)
        for mine in state.planets(my_id):
            strength =  state.garrison(mine)
            if strength > 1 and strength > source_strength:
                source_strength = strength
                source = mine

        # Find the weakest enemy or neutral planet (smallest number of ships).
        for his in (state.planets(u.other(id)) + state.planets(0)):
            strength = state.garrison(his)
            if strength < dest_strength:
                dest_strength = strength
                dest = his

        if source is None or dest is None:
            return None

        return source.id(), dest.id()

