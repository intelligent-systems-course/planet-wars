import api.util as u
from api import Planet
from api.util import SPEED

class Fleet:
    """
    An object representing a collection of ships in transit between planets.

    """

    # Source planet
    # NB this is not strictly necessary to remember, but it's good for debugging
    # and visualization
    __source = None # type: Planet

    # Target planet
    __target = None # type: Planet

    # Distance to the planet
    __distance = None # type: int

    # If owner is player 1
    __ownedBy1 = None # type: bool

    # Number of ships in the fleet
    __size = None # type: int

    # Constructor
    def __init__(self,
                 source,        # type: Planet
                 target,        # type: Planet
                 owner,         # type: int
                 size,          # type: size
                 distance=None  # type: float
            ):
        """
        :param source: The source planet
        :param target: tuple The destination of the fleet
        :param distance: double How far the fleet is from the target.
            If None, the fleet is assumed to be at the source,
            and the distance is computed automatically.
        :param int owner: The owner of the fleet; 1 or 2
        :param int size: The number of ships in the fleet.
        """

        self.__source = source
        self.__target = target
        self.__distance = int(u.distance(source, target) / SPEED) if distance is None else distance
        self.__ownedBy1 = (owner == 1)
        self.__size = size

    def source(self):
        # type: () -> Planet
        """
        :return: The source planet of this fleet
        """
        return self.__source

    def target(self):
        # type: () -> Planet
        """
        :return: The target planet of this fleet
        """
        return self.__target

    def distance(self):
        # type: () -> float
        """
        :return: The distance to the target planet (in plies)
        """
        return self.__distance # type: int

    def owner(self):
        # type: () -> int
        """
        :return: The owner of the fleet (1 or 2)
        """
        return 1 if self.__ownedBy1 else 2;

    def size(self):
        # type: () -> int
        """
        :return: The number of ships in the fleet
        """
        return self.__size # type: int

    def next(self):
        # type: () -> Fleet
        """
        Returns the fleet object represting this fleet one step ahead: ie. with
        the distance decreased by one step.

        :return: A fleet object that represents the same fleet, one turn later. None
            if the fleet has arrived.
        """

        distance = self.__distance - 1

        if distance <= 0:
            return None

        return Fleet(self.__source, self.__target, self.owner(), self.__size, distance)

    def clone(self):
        return Fleet(self.__source, self.__target, self.owner(), self.__size, self.__distance)

    def __repr__(self):
        # type: () -> str
        """
        :return: A compact string representation of this fleet.
        """
        return '[{}>{} s{} o{} d{}]'.format(
            self.__source.id(),
            self.__target.id(),
            self.__size,
            self.owner(),
            self.__distance,
            0)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return hash(self) == hash(other)
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((self.__source.id(), self.__target.id(), self.__distance, self.__ownedBy1, self.__size))
