"""
Check that the minmax bot and alpha beta bot return the same judgement, and that alphabeta bot is faster

"""

from api import State, util
import random, time

from bots.smt import alphabeta
from bots.smt import smt

REPEATS = 10
for DEPTH in (3, 4, 5, 6):
    print 'DEPTH is {}'.format(DEPTH)
    for MOVES in (5, 13, 17):

        ab = alphabeta.Bot(randomize=False, depth=DEPTH)
        sm = smt.Bot(randomize=False, depth=DEPTH)

        ab_time = 0
        sm_time = 0

        ab_info = {}
        sm_info = {}

        for r in range(REPEATS):

            # Generate a start state
            state, id = State.generate(6)

            # Do a few random moves
            for m in range(MOVES):
                state = state.next(random.choice(state.moves()))

            # Ask both bots their move
            # (and time their responses)

            start = time.time()
            sm_move = sm.get_move(state, info=sm_info)
            sm_time += (time.time() - start)

            start = time.time()
            ab_move = ab.get_move(state, info=ab_info)
            ab_time += (time.time() - start)


            if sm_move != ab_move:
                print('Difference of opinion! Minimax said: {}, alphabeta said: {}. State: {}'.format(sm_move, ab_move, state))
            else:
                print('Agreed.')

        print('Done.                  time   Alphabeta: {}, time SMT: {}.'.format(ab_time/REPEATS, sm_time/REPEATS))
        print('      average nodes visited   Alphabeta: {}, time SMT: {}.'.format(float(ab_info['nodes_visited'])/REPEATS, float(sm_info['nodes_visited'])/REPEATS))

        print('SMT speedup: {} '.format(ab_time/sm_time))

