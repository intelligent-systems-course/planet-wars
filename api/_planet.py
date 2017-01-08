import math

class Planet:
    """
    A data object representing a single planet.

    This object contains only the map information, not the information that 
    changed as the game is played (ie. ownership and number of ships stationed).s
    """

    # The coordinates of the planet
    __coords = (-1.0, -1.0)

    # The size of the planet
    __size = -1

    # The id (the index in the map's planets array)
    __id = None

    def __init__(self,
                 x,     # type: float
                 y,     # type: float
                 size,  # type: int
                 id     # type: int
                ):
        """
        :param x: The horizontal coordinate (between 0.0 and 1.0)
        :param y: The vertical coordinate (between 0.0 and 1.0)
        :param size: Size is a value between 0.0 and 1.0. A planet of size 1/n produces a ship once every n turns.
        :param id: The id of this planet in the map's planet's list.
        """

        self.__coords = (x, y)
        self.__size = size
        self.__id = id


    def coords(self):
        # type: () -> Tuple[float]
        """
        Get the coordinates of the given planet

        :return:    A pair of float values between 0 and 1 representing the center
                    point of the planet in the playing area. The playing area is
                    a square with corners (0.0, 0.0) and (1.0, 1.0).
        """
        return self.__coords

    def size(self):
        # type: () -> float
        """
        Get the size of the planet. A planet of size 1/n produces one ship every n turns.

        :return:    An integer in  the range (0, 1), indicating the size and
            of the planet.
        """
        return self.__size
    
    def id(self):
        # type: () -> int
        """
        The index of this planet in the map's planet list.
        :return:
        """
        return self.__id

    def turns_per_ship(self):
        # type: () -> int
        """
        :return: How many turns the owner of this planet needs to wait for a new ship
        """
        return math.floor(1.0/self.__size)

    def __repr__(self):
        # type: () -> str
        """
        :return: A compact string representation of this Planet
        """
        return '[{}: s1/{} {}:{}]'.format(self.__id, self.turns_per_ship(), self.__coords[0], self.__coords[1])