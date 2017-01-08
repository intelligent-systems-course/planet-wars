#!usr/bin/env python
"""
A command line program for multiple games between several bots.

For all the options run
python play.py -h
"""

from argparse import ArgumentParser
from api import State, util, engine
import random

def run_tournament(options):

    botnames = options.players.split(",")

    bots = []
    for botname in botnames:
        bots.append(util.load_player(botname))

    n = len(bots)
    wins = [0] * len(bots)
    matches = [(p1, p2) for p1 in range(n) for p2 in range(n) if p1 < p2]

    totalgames = (n*n - n)/2 * options.repeats
    playedgames = 0

    print('Playing {} games:'.format(totalgames))
    for a, b in matches:
        for r in range(options.repeats):

            if random.choice([True, False]):
                p = [a, b]
            else:
                p = [b, a]

            start, _ = State.generate(options.num_planets)

            winner = engine.play(bots[p[0]], bots[p[1]], start, verbose=False, outfile=None)

            if winner is not None:
                winner = p[winner - 1]
                wins[winner] += 1

            playedgames += 1
            print('Played {} out of {:.0f} games ({:.0f}%): {} \r'.format(playedgames, totalgames, playedgames/float(totalgames) * 100, wins))

    print('Results:')
    for i in range(len(bots)):
        print('    bot {}: {} wins'.format(bots[i], wins[i]))


if __name__ == "__main__":

    ## Parse the command line options
    parser = ArgumentParser()

    parser.add_argument("-n", "--num-planets",
                        dest="num_planets",
                        help="How many planets a generated map should have.",
                        default=6)

    parser.add_argument("-p", "--players",
                        dest="players",
                        help="Comma-separated list of player names (enclose with quotes).",
                        default="rand,bully,rdeep")

    parser.add_argument("-r", "--repeats",
                        dest="repeats",
                        help="How many matches to play for each pair of bots",
                        type=int, default=10)

    parser.add_argument("-t", "--max-time",
                        dest="max_time",
                        help="maximum amount of time allowed per turn in seconds (default: 5)",
                        type=int, default=5)

    options = parser.parse_args()

    run_tournament(options)
