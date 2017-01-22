#!/usr/bin/env python
"""


"""

from api import State, util
import random

from kb import KB, Boolean, Integer

class Bot:

    __max_depth = -1
    __randomize = True

    def __init__(self, randomize=True, depth=8):
        self.__randomize = randomize
        self.__max_depth = depth

    def get_move(self, state, info = None):

        # We need integer values for alpha and beta, so we can't use -inf and +inf
        # These are bounds on the possible heuristic values in a game with
        # 100 turns
        n = len(state.planets())
        minval = - n * 200
        maxval = n * 200

        val, move = self.value(state, alpha=minval, beta=maxval, info=info)

        return move # to do nothing, return None

    def value(self, state, alpha=float('-inf'), beta=float('inf'), depth = 0, info = None):
        """
        Return the value of this state and the associated move
        :param State state:
        :param float alpha: The highest score that the maximizing player can guarantee given current knowledge
        :param float beta: The lowest score that the minimizing player can guarantee given current knowledge
        :param int depth: How deep we are in the tree
        :return val, move: the value of the state, and the best move.
        """
        if info is not None: # debug information
            if 'nodes_visited' not in info:
                info['nodes_visited'] = 0
            info['nodes_visited'] += 1


        if state.finished():
            return (1.0, None) if state.winner() == 1 else (-1.0, None)

        if depth == self.__max_depth:
            return heuristic(state), None

        best_value = float('-inf') if maximizing(state) else float('inf')
        best_move = None

        moves = state.moves()

        if self.__randomize:
            random.shuffle(moves)

        for move in moves:

            next_state = state.next(move)
            value, _ = self.value(next_state, alpha, beta, depth = depth + 1, info=info)

            if maximizing(state):
                if value > best_value:
                    best_value = value
                    best_move = move
                    alpha = best_value
            else:
                if value < best_value:
                    best_value = value
                    best_move = move
                    beta = best_value

            # Check our knowledge base to see if we can prune
            if not self.kb_consistent(state, depth, alpha, beta):
                # print 'smt break on ', alpha, beta
                break

        return best_value, best_move

    def kb_consistent(self, state, depth, alpha, beta):
        # type: (State, int, float, float) -> bool
        """
        Check whether the current state contradicts our knowledge.
        (The knowledge base describes what properties a state should satisfy  to be explored)
        """
        v = Integer("v") # the heuristic value when the maximu m depth is reached
        a = Integer("a") # alpha
        b = Integer("b") # beta
        m = Integer("m") # how many ships player one will have (when the heuristic is computed)
        h = Integer("h") # how many ships player two will have

        kb = KB()

        # Add clauses
        ???

        sat = kb.satisfiable()

        return sat

def maximizing(state):
    """
    Whether we're the maximizing player (1) or the minimizing player (2).

    :param state:
    :return:
    """
    return state.whose_turn() == 1

def heuristic(state):
    # type: (State) -> float

    return count_ships(state, 1) - count_ships(state, 2)

def count_ships(state, player):
    # type: (State, int) -> int
    '''
    :param state: A game state
    :param player: a player id
    :return: Counts the number of ships in the game state (in fleets and planets) belonging to the given player.
    '''

    sum = 0

    for planet in state.planets(player):
        sum += state.garrison(planet)
    for fleet in state.fleets():
        if fleet.owner() == player:
            sum += fleet.size()
    return sum
