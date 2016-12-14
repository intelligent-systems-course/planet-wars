import random

class Map:
    """
    A data object representing the map, ie. the coordinates and size of all planets.
    
    More precisely, the map contains all information that is immutable: ie. it 
    does not change throughout the game, as turns are made.
    
    To generate a random map, or load one from a file, see State
     
    """

    """ Private members"""
    # Planets
    __planets = []
    
    # Constructor
    def __init__(self, planets):
        __planets = planets

    """ 
    Compute the distance in plies between two planets. A plie is half a turn, ie.
    one player's move. 
    
    :planet1 int: The index of the first planet
    :planet1 int: The index of the second planet
    
    :return: An int representing the number of half-turns (plies) it will take
        for a fleet to get from one planet to the other.
    """
    def distance(self, planet1, planet2):
        pass
    
    def size(self):
        return len(planets)
        
 