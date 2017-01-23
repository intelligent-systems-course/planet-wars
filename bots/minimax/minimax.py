#!/usr/bin/env python
"""


"""

from api import State, util
import random

class Bot:

    __max_depth = -1
    __randomize = True
    __my_id = 0

    def __init__(self, randomize=True, depth=4):
        """
        :param randomize: Whether to select randomly from moves of equal value (or to select the first always)
        :param depth:
        """
        self.__randomize = randomize
        self.__max_depth = depth

    def get_move(self, state):
        # type: (State) -> tuple[int, int]

        # Find out which player we are
        self.__my_id = state.whose_turn()

        val, move = self.value(state)

        return move # to do nothing, return None

    def value(self, state, depth = 0):
        # type: (State, int) -> tuple[float, tuple[int, int]]
        """
        Return the value of this state and the associated move
        :param state:
        :param depth:
        :return: A tuple containing the value of this state, and the best move for the player currently to move
        """
        if state.finished():
            return (1.0, None) if state.winner() == self.__my_id else (-1.0, None)

        if depth == self.__max_depth:
            return heuristic(state, self.__my_id)

        moves = state.moves()

        if self.__randomize:
            random.shuffle(moves)

        best_value = float('-inf') if maximizing(state, self.__my_id) else float('inf')
        best_move = None

        for move in moves:

            next_state = state.next(move)

            # IMPLEMENT: Add a recursive function call so that 'value' will contain the
            # minimax value of 'next_state'
            value ???

            if maximizing(state, self.__my_id):
                if value > best_value:
                    best_value = value
                    best_move = move
            else:
                if value < best_value:
                    best_value = value
                    best_move = move

        return best_value, best_move

def maximizing(state, my_id):
    # type: (State) -> bool
    """
    :param state:
    :return: True if we're the maximizing player (player 1), false otherwise (player 2).
    """
    return state.whose_turn() == my_id

def heuristic(state, my_id):
    # type: (State) -> float
    """
    Estimate the value of this state: -1.0 is a certain win for player 2, 1.0 is a certain win for player 1

    :param state:
    :return: A heuristic evaluation for the given state (between -1.0 and 1.0)
    """
    return util.ratio_ships(state, my_id) * 2.0 - 1.0, None
