#!usr/bin/env python
"""
A command line program for playing a single game between two bots.

For all the options run
python play.py -h
"""

from argparse import ArgumentParser
import sys

from api import State, engine, util


def call_engine(options):

    # Create player 1
    player1 = util.load_player(options.player1)

    # Create player 2
    player2 = util.load_player(options.player2)

    # Generate or load the map
    state, id = State.generate(int(options.num_planets), symmetric=not options.asym)

    if not options.quiet:
        print('-- Using map with id {} '.format(id))
        print('   Start state: ' + str(state))

    # Play the game
    viz = (options.outputfile.lower() == 'none')
    outfile = options.outputfile # type: str
    if not outfile.endswith('.pdf'):
        outfile += '.pdf'

    engine.play(player1, player2, state=state, max_time=options.max_time*1000, verbose=(not options.quiet), outfile=outfile)

if __name__ == "__main__":

    ## Parse the command line options
    parser = ArgumentParser()

    parser.add_argument("-n", "--num-planets",
                        dest="num_planets",
                        help="How many planets the map should have. (only for generated maps)",
                        default=6)

    # player 1 & 2
    parser.add_argument("-1", "--player1",
                        dest="player1",
                        help="the program to run for player 1 (default: rand)",
                        default="rand")
    parser.add_argument("-2", "--player2",
                        dest="player2",
                        help="the program to run for player 2 (default: bully)",
                        default="bully")

    parser.add_argument("-t", "--max-time",
                        dest="max_time",
                        help="maximum amount of time allowed per turn in seconds (default: 5)",
                        type=int, default=5)

    parser.add_argument("-q", "--quiet", dest="quiet",
                        help="Whether to hide the printed output.",
                        action="store_true")

    parser.add_argument("--output", dest="outputfile",
                        help="Where to store the visualization of the game (a pdf file). Set to 'none' for no output.",
                        default="game.pdf")

    parser.add_argument("-a", "--asym", dest="asym",
                        help="Whether to start with an asymmetric state.",
                        action="store_true")

    options = parser.parse_args()

    call_engine(options)
