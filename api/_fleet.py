import math

from api import Planet
import api.util as u

# It takes ten steps to get from one corner of the map to another
SPEED = math.sqrt(2.0) / 10


class Fleet:
    """
    An object representing a collection of ships in transit between planets.

    """

    """ Private members"""

    # Source planet
    # NB this is not strictly necessary to remember, but it's good for debugging 
    # and visualization
    __source = None # type: Planet
    
    # Target planet
    __target = None # type: Planet
    
    # Distance to the planet
    __distance = None # type: float
        
    # If owner is player 1
    __ownedBy1 = None # type: bool
    
    # Number of ships in the fleet
    __size = None # type: int
    
    # Constructor
    def __init__(self, source: Planet, target: Planet, owner, size, distance=None):
        """
        :param source: tuple
        :param target: tuple The destination of the fleet (a tuple)
        :param distance: double How far the fleet is from the target. If None, the fleet is assumed to be at the source,
            and the distance is computed automatically.
        :param owner: int The owner of the fleet; 1 or 2
        :param size: int The number of ships in the fleet.
        """

        self.__source = source
        self.__target = target
        self.__distance = u.distance(source, target) if distance is None else distance
        self.__owner = owner
        self.__size = size

    def target(self):
        return self.__target # type: Planet
    
    def distance(self):
        return self.__distance # type: float
    
    def owner(self):
        return 1 if self.__ownedBy1 else 2;
    
    def size(self):
        return self.__size # type: int
    
    """
    Returns the fleet object one step ahead: ie. with the distance decreased
    by one step
    
    :return: A fleet object that represents the same fleet, one turn later. None
        if the fleet has arrived.
    """
    def next(self):
        fleet = Fleet()
        
        fleet.__source = self.__source
        fleet.__target = self.__target
        fleet.__speed = self.__speed
        fleet.__ownedBy1 = self.__ownedBy1
        fleet.__size = self.__size
        
        fleet.__distance = self.__distance - SPEED
        
        if fleet.__distance < 0.0:
            return None
        return fleet # type: Fleet
        
    