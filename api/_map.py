import random


class Map:
    """
    A data object representing the map, ie. the coordinates and sizes of all planets.
    
    More precisely, the map contains all information that is static: ie. it
    does not change throughout the game, as turns are made.
    
    To generate a random map, or load one from a file, see State
    """

    # Planets
    __planets = None # type: list[Planet]
    
    def __init__(self, planets):
        """
        :param planets: A list of the planets for this map. The list is
            copied and the resultant Map object is not back by the given list.
        """
        self.__planets = list(planets)

    def planets(self):
        """
        :return: A list of the planets in this map.
        """
        return self.__planets
    
    def size(self):
        # type: () -> int
        """
        :return: The number of planets in this map
        """
        return len(self.__planets)
        
 