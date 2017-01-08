"""
Train a machine learning model for the classifier bot. We create a player, and watch it play games against itself.
Every observed state is converted to a feature vector and labeled with the eventual outcome
(-1.0: player 2 won, 1.0: player 1 won)

This is part of the second worksheet.
"""
from api import State, util

# This package contains various machine learning algorithms
import sklearn
import sklearn.linear_model
from sklearn.externals import joblib

from bots.rand import rand
# from bots.alphabeta import alphabeta
from bots.ml import ml

from bots.ml.ml import features

import matplotlib.pyplot as plt

# How many games to play
GAMES = 1000
# Number of planets in the field
NUM_PLANETS = 6

# The player we'll observe
player = rand.Bot()
# player = alphabeta.Bot()

data = []
target = []

for g in range(GAMES):

    state, id = State.generate(NUM_PLANETS)

    state_vectors = []
    while not state.finished():

        state_vectors.append(features(state))

        move = player.get_move(state)
        state = state.next(move)

    winner = state.winner()

    for state_vector in state_vectors:
        data.append(state_vector)
        target.append('won' if winner == 1 else 'lost')

    if g % (GAMES/10) == 0:
        print('game {} finished ({}%)'.format(g, (g/float(GAMES)*100) ))

# Train a logistic regression model
learner = sklearn.linear_model.LogisticRegression()
model = learner.fit(data, target)

# Check for class imbalance
count = {}
for str in target:
    if str not in count:
        count[str] = 0
    count[str] += 1

print('instances per class: {}'.format(count))

# Store the model in the ml directory
joblib.dump(model, './bots/ml/model.pkl')

print('Done')




