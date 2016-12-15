import math


def other(player_id: int):
    """
    Returns the index of the opposite player to the one given: ie. 1 if the argument is 2 and 2 if the argument is 1.
    :param player:
    :return:
    """
    return 1 if player_id == 2 else 2 # type: int


def distance(source: tuple, target: tuple):
    """
    Computes the (Euclidean) distance between to 2D points.
    :param source:
    :param target:
    :return:
    """
    dx = source[0] - target[0]
    dy = source[1] - target[1]

    return math.sqrt(dx**2 + dy**2) # type: tuple
