"""
General utility functions
"""

import math, sys, os
from api import Planet
import importlib

def other(
        player_id # type: int
        ):
    # type: () -> int
    """
    Returns the index of the opposite player to the one given: ie. 1 if the argument is 2 and 2 if the argument is 1.
    :param player:
    :return:
    """
    return 1 if player_id == 2 else 2 # type: int


def distance(
        source, # type: Planet
        target  # type: Planet
        ):
    # type: () -> float
    """
    :param source:
    :param target:
    :return: the (Euclidean) distance between two 2D points.
    """

    dx = source.coords()[0] - target.coords()[0]
    dy = source.coords()[1] - target.coords()[1]

    return math.sqrt(dx**2 + dy**2)


def ratio_ships(state, owner_id):
    # type: () -> float
    """
    :return: the ratio of the number of ships belonging to given player to the total
    """
    p1ships = 0
    totalships = 0

    # Count the planets
    for planet in state.planets():
        totalships += state.garrison(planet)
        if state.owner(planet) == owner_id:
            p1ships += state.garrison(planet)

    # Count the fleets
    for fleet in state.fleets():
        totalships += fleet.size()
        if fleet.owner() == owner_id:
            p1ships += fleet.size()

    return float(p1ships) / float(totalships)


def combine_heuristics(*args):
    """
    Combines heuristics with varying weights.
    Example:
    combine_heuristics((0.2, 1.0), (0.8, -1.0)) -> -0.6


    :param args: Tuples in the form (weight, value)
    :type args: Tuple[Tuple[float, float]]
    :return: value in the range -1.0..1.0
    :rtype: float
    """

    return max(-1.0, min(1.0, reduce(lambda a, (w, h): a + (w * h), args, 0)))

def load_player(name, classname='Bot'):
    #
    """
    Accepts a string representing a bot and returns an instance of that bot. If the name is 'random'
    this function will load the file ./bots/random/random.py and instantiate the class "Bot"
    from that file.

    :param name: The name of a bot
    :return: An instantiated Bot
    """
    name = name.lower()
    path = './bots/{}/{}.py'.format(name, name)

    # Load the python file (making it a _module_)
    try:
        module = importlib.import_module('bots.{}.{}'.format(name, name))
    except:
        print('ERROR: Could not load the python file {}, for player with name {}. Are you sure your Bot has the right filename in the right place? Does your python file have any syntax errors?'.format(path, name))
        sys.exit(1)

    # Get a reference to the class
    try:
        cls = getattr(module, classname)
        player = cls() # Instantiate the class
        player.__init__()
    except:
        print('ERROR: Could not load the class "Bot" {} from file {}.'.format(classname, path))
        sys.exit()

    return player

"""
The universal speed of a spaceship: ie. how much each fleet moves per plie.

(This just says that it moves from one corner of the playing field to the other in ten plies)
"""
SPEED = math.sqrt(2.0) / 10
