import matplotlib as mpl
mpl.use('Agg')
import matplotlib.axes as axes
import matplotlib.pyplot as plt
import api
import random
import api.util as u
import copy
import math

from api import Fleet, Planet, Map


class State:
    """
    Represents the state of the game at a given plie.
    """

    # The map
    __map = None # type: Map

    # Whether each planet belongs to player 1, 2 or is neutral (player 0)
    __owner = [] # type: list[int]

    # The number of ships stationed at each planet
    __garrisons = [] # type: list[int]

    # All fleets in transit
    __fleets = [] # type: list[Fleet]

    # True if it's player 1's turn
    __player1s_turn = None # type: bool

    # If one of the players has lost the game by making an illegal move
    # or not moving fast enough. None is nobody has revoked, otherwise the
    # id of the player that revoked
    __revoked = None # type: int, None

    # How many turns have passed
    __turn = 0 # type: int

    def __init__(self,
                 map,           # type: Map
                 garrisons,     # type: list[int]
                 owner,         # type: int
                 start=1,       # type: int
                 fleets=None    # type: list[Fleet]
                ):
        """
        :param map:         The playing area
        :param garrisons:   A list of integers such that garrisons[i]
            contains the number of ships stationed at planet map.planets()[i]
        :param owner:       A list of integers such that owners[i]
            contains the owner (0, 1 or 2) of planet  map.planets()[i]
        :param start:       Which player is set to make the next turn in this state (1 or 2)
        :param fleets:      A list of fleet objects representing the fleets in transit in this state
        """
        self.__map = map
        self.__owner = list(owner)

        self.__garrisons = list(garrisons)

        self.__player1s_turn = True if start == 1 else False

        if not fleets is None:
            self.__fleets = list(fleets)

    @classmethod
    def make(cls,
             map,               # type: Map
             garrisons,         # type: list[int]
             player1s_planets,  # type: list[int]
             player2s_planets,  # type: list[int]
             start=1,           # type: int
             fleets=None        # type: list[Fleet]
            ):
        """
        A factory method allowing you to construct a state by specifying the planets owned by
        each players in two separate lists.

        :param map:         The playing area
        :param garrisons:   A list of integers such that garrisons[i]
            contains the number of ships stationed at planet map.planets()[i]
        :param player1s_planets: A list containing the indices of the planets
            belonging to player 1
        :param player2s_planets: A list containing the indices of the planets
            belonging to player 2
        :param start: Which play is set to make the next move (1 or 2)
        :param fleets: A list of fleet objects representing the fleets in transit in this state
        :return:
        """
        owner = [0] * map.size()

        for i in player1s_planets:
            owner[i] = 1

        for i in player2s_planets:
            owner[i] = 2

        return cls(map, list(garrisons), owner, start, fleets)

    def fleets(self):
        # type: () -> list[Fleet]
        """
        :return: A list of the fleet objects in this state
        """
        return list(self.__fleets)

    def next(self,
             move   # type: tuple[int, int]
            ):
        # type: () -> State
        """
        Compute the next state from this one, assuming that the player whose turn it is makes the given move.

        :return: The state that would result from the given move.
        :raises: RuntimeError if state is finished. Be sure to check state.finished() before calling this
            method.
        """

        if self.finished():
            raise RuntimeError('Gamestate is finished. No next states exist.')

        # Start with a copy of the current state
        state = self.clone() # type: State

        # Switch the player
        state.__player1s_turn = not self.__player1s_turn

        # Increment the turn number (we count the number of turns not of plies)
        if self.whose_turn() == 2:
            state.__turn += 1

        # Check illegal moves (moving from other player's planet)
        if move is not None and self.owner(self.planets()[move[0]]) != self.whose_turn():
            state.__revoked = self.whose_turn()
            return state

        state.__fleets = []

        # Execute the move
        if move is not None:

            source = self.planets()[move[0]]
            target = self.planets()[move[1]]

            if self.garrison(source) > 1: # If the source planet has < 1 ships, no fleet is sent

                half = float(self.__garrisons[source.id()]) * 0.5
                fleetsize =  int(math.floor(half))  # add half the ships to the fleet
                state.__garrisons[source.id()] = self.__garrisons[source.id()] - fleetsize  # leave the rest behind

                fleet = Fleet(source, target, self.whose_turn(), fleetsize)
                state.__fleets.append(fleet)

        # Move the fleets, and handle attacks
        for fleet in self.__fleets:

            next = fleet.next() # New fleet object, one step closer to destination

            if next is None: # fleet has arrived

                # Reinforcements
                if state.owner(state.planets()[fleet.target().id()]) == fleet.owner():
                    state.__garrisons[fleet.target().id()] += fleet.size()

                # Attack
                else:
                    # compute the ships remaining after attack: negative means attacker won
                    result = state.__garrisons[fleet.target().id()] - fleet.size()

                    # Planet is conquered, change owner
                    if result < 0:
                        state.__owner[fleet.target().id()] = fleet.owner()
                        state.__garrisons[fleet.target().id()] = - result
                    else:
                        state.__garrisons[fleet.target().id()] = result
            else:
                state.__fleets.append(next)


        state.__player1s_turn = not self.__player1s_turn

        # If player 2 has moved (end of the turn), increase the garrisons
        if self.whose_turn() == 2:
            for planet in self.planets():

                if self.__turn % planet.turns_per_ship() == 0 \
                        and self.owner(planet) != 0 \
                        and self.__turn != 0:
                    state.__garrisons[planet.id()] += 1

        return state

    def turn_nr(self):
        # type: () -> int
        """
        :return: How many turns preceded this state.
        """
        return self.__turn

    def whose_turn(self):
        # type: () -> int
        """
         :return: The player who is set to make the next move.
         """
        return 1 if self.__player1s_turn else 2

    def planets(self,
            owner_id = None # type: int
            ):
        # type: () -> list[Planet]
        """
        :param owner_id: Filter by owner. If given, only the planets belonging to
            this owner are returned (0, 1 or 2)
        :return: a list of planets. If no id is given, return all planets. With an
        id (0, 1 or 2), all planets belonging to that player
        """
        planets = self.__map.planets()

        if owner_id is None:
            return planets

        return [p for p in planets if self.owner(p) == owner_id]

    def finished(self):
        # type: () -> bool
        """
        :return: A boolean indicating whether the game is finished. The game
        is finished if one of the players has zero ships left, or if a player
        has revoked. A player revokes by playing an illegal move, or not
        finishing on time (in a time controlled game).
        """

        if self.__revoked is not None:
            return True

        for owner in [1, 2]:
            # If no planets owned
            if len(self.planets(owner)) == 0:

                # check nr of fleets owned
                fleets = 0
                for fleet in self.__fleets:
                    if fleet.owner() == owner:
                        fleets += 1

                if fleets == 0:
                    return True

        return False

    def revoked(self):
        return self.__revoked

    def winner(self):
        """
        Who won the game (if it's finished).

        :return: The (integer) id of the player who won if the game is finished (1 or 2). None
            if the game is not finished.
        """
        if not self.finished():
            return None

        if self.__revoked is not None:
            return self.whose_turn()

        if len(self.planets(1)) == 0:
            return 2

        assert(len(self.planets(2)) == 0)

        return 1

    def owner(self,
              planet # type: Planet
            ):
        # type: () -> int
        """
        :param planet: The planet for which we want the owner (NB: the planet object, not the id)
        :return: who owns the given planet in this gamestate.
        """
        return self.__owner[planet.id()] # type: int

    def garrison(self,
            planet   # type: Planet
        ):
        """
        :param planet: The planet for which we want the number of stationed ships.
        :return: How many ships there are at the given planet in this gamestate
        """

        return self.__garrisons[planet.id()]

    def clone(self):
        # type: () -> State
        """
        Creates a copy of this state object, where all the volatile
        objects (fleets, owner array) are deep-copied. The map and planet are
        references to the original objects.
        """
        state = State(self.__map, list(self.__garrisons), list(self.__owner))

        state.__revoked = self.__revoked

        # Deep copy the fleets
        fleets = [fleet.clone() for fleet in self.__fleets]
        state.__fleets = fleets

        state.__turn = self.__turn

        return state

    def moves(self):
        # type: () -> list[tuple[int, int]]
        """
        :return: A list of all the legal moves that can be made by the player whose turn it is.
        """
        # get the planets
        mine = self.planets(self.whose_turn())
        all = self.planets()

        # Generate all possible pairs with the first element from mine
        # and the second from all.
        moves = []
        for m in mine:
            if self.garrison(m) > 1:
                for a in all:
                    if m.id() != a.id():
                        moves.append((m.id(),a.id()))

        # None is also a legal move (do nothing)
        moves.append(None)

        return moves

    def visualize(self):
        # type: () -> Figure
        """
        Visualize the gamestate.

        :return: A matplotlib figure object. Save to a file with::
            state.visualize().savefig('filename.png')

            The format is automatically determined from the extension you choose.
        """
        fig = plt.figure(figsize=(6,6))
        cm = ['gray', 'blue', 'red']

        ax = fig.add_subplot(111) # type: axes.Axes
        ax.set_axis_bgcolor('#19102b')

        # Plot the planets
        xs = []
        ys = []
        sizes = []
        labels = []

        for planet in self.planets():
            xs.append(planet.coords()[0])
            ys.append(planet.coords()[1])
            sizes.append(planet.size() * 500)
            labels.append(self.garrison(planet))

        ax.scatter(xs, ys, s=sizes, c=[cm[o] for o in self.__owner], zorder=10, linewidth=0,)

        for x, y, label, size in zip(xs, ys, labels, sizes):
            ax.annotate(
                label,
                xy=(x, y), xytext=(0, - 15 - size/50.0),
                textcoords='offset points', ha='center', va='bottom',
                zorder=30, color='white')

        # Plot the fleets
        for fleet in self.__fleets:
            ax.plot(
                [fleet.source().coords()[0],
                 fleet.target().coords()[0]],
                [fleet.source().coords()[1],
                 fleet.target().coords()[1]], alpha=0.8, color=cm[fleet.owner()], linestyle='dotted')

            turns_left = fleet.distance()
            max_dist = api.util.distance(fleet.source(), fleet.target())
            max_turns = max_dist / u.SPEED

            ratio = 0.5 if max_turns == 0 else float(turns_left) / float(max_turns) # scale the distance travelled to target to the range (0, 1)

            # Current location of the fleet
            location = plus(mult(fleet.source().coords(), ratio), mult(fleet.target().coords(), 1.0 - ratio))

            ax.scatter(location[0], location[1], c=cm[fleet.owner()], s=math.sqrt(fleet.size()) * 20, marker='s', linewidth=0, zorder=20)

            ax.annotate(
                fleet.size(),
                xy=location, xytext=(0, - 20),
                textcoords='offset points', ha='center', va='bottom',
                zorder=30, color=cm[fleet.owner()])

        ax.spines["right"].set_visible(False)
        ax.spines["top"].set_visible(False)
        ax.spines["bottom"].set_visible(False)
        ax.spines["left"].set_visible(False)

        ax.get_xaxis().set_tick_params(which='both', top='off', bottom='off', labelbottom='off')
        ax.get_yaxis().set_tick_params(which='both', left='off', right='off', labelleft='off')

#        ax.set_xlim([0, 1])
#        ax.set_ylim([0, 1])

        ax.set_title('turn {}.{}: '.format(self.__turn, self.whose_turn()))

        return fig

    def __repr__(self):
        # type: () -> str
        """
        :return: A concise string representation of the state in one line
        """
        res = 'turn {}.{}: '.format(self.__turn, self.whose_turn())
        res += ' planets: '

        for i, planet in enumerate(self.planets()):
            res += ', ' if i !=0 else ''
            res += '{}.o{}g{}'.format(planet.id(), self.owner(planet), self.garrison(planet))

        if len(self.fleets()) == 0:
            res += '\t no fleets'
        else:
            res += '\t fleets: '
            for i, fleet in enumerate(self.fleets()):
                res += ', ' if i !=0 else ''
                res += '{}>{}.o{}s{}d{}'.format(
                    fleet.source().id(), fleet.target().id(),
                    fleet.owner(), fleet.size(), fleet.distance())

        return res

    @staticmethod
    def generate(num_planets, id=None, symmetric=True):
        # type: () -> (State, id)
        """
        Generates a random start state: a random map, with home planets assigned
        NB: This method returns a tuple (State, id), so call it like this::

            state, id = State.generate(6)

        :param num_planets: The number of planets in the map
        :param id: Optional. The same id will always lead to the same map. If it is not
            supplied, or None, a random map will be generated.

        :return: A pair of a starting state and its id.
        """

        if not symmetric:
            return State.generate_asym(num_planets, id)

        if id is None:
            id = random.randint(0, 100000)

        # Create an RNG with id as the seed
        rng = random.Random(id)

        planets = []

        # Home planets
        planets.append(Planet(0.0, 0.0, 1, 0))
        planets.append(Planet(1.0, 1.0, 1, 1))

        garrisons = [100, 100]

        # Rest of the planets
        for i in range(2, num_planets, 2):
            x = round(rng.random(), 2)
            y = round(rng.random(), 2)
            size = 1.0 / rng.choice([1] + [3, 5, 7, 13, 17] * 3)

            garrisons += ([rng.randint(1, 30)] * 2)
            planets.append(Planet(x, y, size, i))
            planets.append(Planet(1 - x, 1 - y, size, i + 1))

        if num_planets % 2 != 0:
            x = round(rng.random(), 2)
            y = 1 - x
            size = 1.0 / rng.choice([1] + [3, 5, 7, 13, 17] * 3)

            garrisons.append(rng.randint(1, 30))
            planets.append(Planet(x, y, size, num_planets - 1))

        map = Map(planets)

        state = State.make(map, garrisons, [0], [1])

        return state, id

    @staticmethod
    def generate_asym(num_planets, id=None):
        if id is None:
            id = random.randint(0, 100000)

            # Create an RNG with id as the seed
        rng = random.Random(id)

        planets = []

        # Home planets
        planets.append(Planet(0.0, 0.0, 1, 0))
        planets.append(Planet(1.0, 1.0, 1, 1))

        garrisons = [100, 100]

        # Rest of the planets
        for i in range(num_planets):
            x = round(rng.random(), 2)
            y = round(rng.random(), 2)
            size = 1.0 / rng.choice([1] + [3, 5, 7, 13, 17] * 3)

            garrisons.append(rng.randint(1, 30))
            planets.append(Planet(x, y, size, i))

        if num_planets % 2 != 0:
            x = round(rng.random(), 2)
            y = 1 - x
            size = 1.0 / rng.choice([1] + [3, 5, 7, 13, 17] * 3)

            garrisons.append(rng.randint(1, 30))
            planets.append(Planet(x, y, size, num_planets - 1))

        map = Map(planets)

        state = State.make(map, garrisons, [0], [1])

        return state, id

    @staticmethod
    def load(file, whose_turn=1):
        # type: () -> State
        """
        Loads a state from a file (or more accurately, a map, and garrison/ownership information).

        Each line in the file describes a planet. The lines should be of the form
            x, y, size, nr_ships, owner
        At least one planet should be owned by player 1 and one by 2.

        For instance:
            0.0, 0.0, 10, 50, 1
            1.0, 1.0, 10, 50, 2
            0.5, 0.5, 1, 30, 0
        """

        planets = []
        garrisons = []
        owners = []

        with open(file, 'r') as f:
            for line in f:
                line = line.rstrip()
                x, y, size, nr_ships, owner = line.split(',')

                x = float(x)
                y = float(y)
                size = int(size)
                nr_ships = int(nr_ships)
                owner = int(owner)

                planets.append(Planet(x, y, size))
                garrisons.append(nr_ships)
                owners.append(owner)

        map = Map(planets)
        state = State(map, garrisons, owners, whose_turn)

def mult(
        seq,    # type: list[float]
        scalar  # type:
        ):
    # type: () -> list[float]
    """
    Create a list by multiplying seq element-wise by scalar.
    :param seq:
    :param scalar:
    :return: A list with the value seq[i] * scalar at index i
    """
    return [value * scalar for value in seq]


def plus(pair1, pair2):
    # type: () -> tuple
    """
    Element-wise sum for pairs
    :return: A pair; the element-wise sum of the given pairs
    """
    return pair1[0] + pair2[0], pair1[1] + pair2[1]
