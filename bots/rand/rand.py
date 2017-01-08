#!/usr/bin/env python

"""
RandomBot -- A simple strategy: enumerates all legal moves, and picks one 
uniformly at random.
"""

# Import the API objects
from api import State
import random


class Bot:

    def __init__(self):
        pass

    def get_move(self, state):
        # type: (State) -> tuple[int, int]
        """
        Function that gets called every turn. This is where to implement the strategies.

        Be sure to make a legal move. Illegal moves, like giving a source planet you
        don't own, will lose you the game.

        If you return a source and destination, 50% of the ships of the source
        planet (rounded down) will be sent to the destination. If that planet is
        owned by the enemy or neutral when they arrive, they will attack it, if it is
        owned by you, they will reinforce it (add to the number of ships stationed).

        :param State state: An object representing the gamestate. This includes a link to the
            map, ownership of each planet, garrisons on each plant, and all fleets in transit.

        :return: None, indicating no move is made, or a pair of integers,
            indicating a move; the first indicates the source planet, the second the
            destination.
        """

        # All legal moves
        moves = state.moves()

        # Return a random choice
        return random.choice(moves)
