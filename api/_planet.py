
class Planet:
    """
    A data object representing a single planet.

    This object contains only the map information, not the information that 
    changed as the game is played (ie. ownership and number of ships stationed).s
    """

    """ Private members """
    # The coordinates of the planet
    __coords = (-1.0, -1.0)

    # The size of the planet
    __size -= -1

    # The id (the index in the map's planets array)
    __id = None

    def __init__(x, y, size, id):
        __coords = (x, y)
        __size = size
        __id = id

    """
    Get the coordinates of the given planet
        
    :return:    A pair of decimal values between 0 and 1 representing the center 
                point of the planet in the playing area. The playing area is 
                a square with corners (0.0, 0.0) and (1.0, 1.0).
    """
    def coords(self):
        return __coords
    
    """
    Get the size of the planet. The size is expressed as the production capacity:
    how many new ships the planet generates per plie.
        
    :return:    An integer in  the range (1, 10), indicating the size and 
        production caopacity of the planet.
    """
    def size(self):
        return __coords
    
    def id(self):
        return id