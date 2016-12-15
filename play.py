#!usr/bin/env python
"""
A command line program for playing a single game between two bots.

For all the options run
python play.py -h
"""

from argparse import ArgumentParser
import importlib.util
import sys

from api import State, engine

def call_engine(options):

    # Create player 1
    player1 = load_player(options.player1)

    # Create player 2
    player2 = load_player(options.player2)

    # Generate or load the map
    state, id = State.generate(options.num_planets)
    if not options.quiet:
        print('-- Using map with id {} '.format(id))

    # Play the game
    viz = (options.outputfile.lower() == 'none')
    outfile = options.outputfile # type: str
    if not outfile.endswith('.pdf'):
        outfile += '.pdf'

    engine.play(player1, player2, state=state, max_time=options.max_time, verbose=(not options.quiet), visualize=viz, outfile=outfile)


def load_player(name : str):
    """
    Accepts a string representing a bot and returns an instance of that bot. If the name is 'random'
    this function will instantiate the class RandomBot in the file ./random/RandomBot.py . It will not look anywhere
    else.

    :param name:
    :return:
    """
    name = name.lower()

    classname = name.capitalize()
    path = './{}/{}.py'.format(name, classname)


    # Load the python file (making it a _module_)
    try:
        spec = importlib.util.spec_from_file_location(classname, path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    except:
        print('ERROR: Could not load the python file {}, for player with name {}. Are you sure your Bot has the right filename in the right place?'.format(path, name))
        sys.exit(1)

    # Get a reference to the class
    try:
        cls = getattr(module, classname)
        player = cls() # Instantiate the class
    except:
        print('ERROR: Could not load the class {} from file {}.'.format(classname, path))
        sys.exit()



    return player

if __name__ == "__main__":

    ## Parse the command line options
    parser = ArgumentParser()

    # map option (relative paths)
    parser.add_argument("-m", "--map",
                        dest="map",
                        help="The map to play on",
                        default="random")

    parser.add_argument("-n", "--num-planets",
                        dest="num_planets",
                        help="How many planets the map should have. (only for generated maps)",
                        default=12)

    # player 1 & 2, I want only the bare minimum to be mentioned here (EmptyBot.py for instance)
    parser.add_argument("-1", "--player1",
                        dest="player1",
                        help="the program to run for player 1 (default: random)",
                        default="random")
    parser.add_argument("-2", "--player2",
                        dest="player2",
                        help="the program to run for player 2 (default: random)",
                        default="random")

    parser.add_argument("-t", "--max-time",
                        dest="max_time",
                        help="maximum amount of time allowed per turn in msec (default: 5000)",
                        type=int, default=5000)

    parser.add_argument("-x", "--max-turns", dest="max_turns",
                        help="maximum amount of turns in a game  (default: 100)",
                        type=int, default=100)

    parser.add_argument("-q", "--quiet", dest="quiet",
                        help="Whether to hide the printed output.",
                        action="store_true")

    parser.add_argument("--output", dest="outputfile",
                        help="Where to store the visualization of the game (a pdf file). Set to 'none' for no output.",
                        default="game.pdf")

    options = parser.parse_args()

    call_engine(options)
