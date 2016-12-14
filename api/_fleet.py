import math

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
    __source = None
    
    # Target planet
    __target = None
    
    # Distance to the planet
    __distance = None
        
    # If owner is player 1
    __ownedBy1 = None
    
    # Number of ships in the fleet
    __size = None
    
    # Constructor
    def __init__(self, source, target, distance, owner, size):
        pass
    
    def target(self):
        return target
    
    def distance(self):
        return distance
    
    def owner(self):
        return 1 if ownedBy1 else 2;
    
    def size(self):
        return size
    
    """
    Returns the fleet object one step ahead: ie. with the distance decreased
    by one step
    
    :return: A fleet object that represents the same fleet, one turn later. None
        if the fleet has arrived.
    """
    def next(self):
        fleet = Fleet()
        
        fleet.__source = __source
        fleet.__target = __target
        fleet.__speed = __speed
        fleet.__ownedBy1 = fleet.__ownedBy1
        fleet.__size = fleet.__size
        
        fleet.__distance = __distance - SPEED
        
        if fleet.__distance < 0.0:
            return None
        return fleet
        
    