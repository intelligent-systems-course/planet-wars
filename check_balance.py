"""
How biased are the generated states? Does one player have a clear advantage?

To check this for random-moving players we generate a random state, and play 100 random
games (ie. each move is a random choice). This gives us an estimate of the proportion
of terminal nodes in the game tree where player 1 wins. If this proportion is close to
0.5, the state is reasonably fair.

"""

from api import State
import random
import matplotlib.pyplot as plt

SAMPLES = 100
REPEATS = 100

result = []
for r in range(REPEATS):
    if r % 10 == 0:
        print('repeat {}'.format(r))

    # Generate a random start state
    start_state, id = State.generate(num_planets=6)

    # Count how many games are won by player 1
    won_by_1 = 0

    for i in range(SAMPLES):

        state = start_state.clone()

        while not state.finished():
            random_move = random.choice(state.moves())
            state = state.next()

        if state.winner() == 1:
            won_by_1 += 1

    result.append( won_by_1/float(SAMPLES) )

# Create a simple plot using matplotlib
plt.hist(result)
plt.xlim([0, 1])
plt.savefig('balance.png')