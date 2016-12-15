import matplotlib as mpl
import matplotlib.axes as axes
import matplotlib.pyplot as plt
import api
import random
import api.util as u
import copy
import math

from api import Fleet, Planet, State
from typing import List

class State:
    """
    Represents the state of the game at a given plie.
    """

    # The map
    """ :type: api.Map"""
    __map = None
    
    # Whether each planet belongs to player 1, 2 or is neutral (0)
    __owner = []
    
    # The number of ships stationed at each planet
    __garrisons = []
    
    # All fleets in transit
    __fleets = []

    # True if it's player 1's turn 
    __player1s_turn = None #type: bool
    
    # If one of the players has lost the game by making an illegal move
    # or not moving fast enough.
    __revoked = None # type: int, None
    
    def __init__(self, map, garrisons, player1s_planets, player2s_planets, start=1, fleets=None):
        owner = [0] * map.size()

        for i in player1s_planets:
            owner[i] = 1
            
        for i in player2s_planets:
            owner[i] = 2
            
        __garrisons = list(garrisons)
                
        player1s_turn = True if start == 1 else False
        

    def next(self, move):
        """
        Returns the state that would result from the given move.

        :raises: RuntimeError if state is finished
        :rtype: api.State
        """

        if self.finished():
            raise RuntimeError('Gamestate is finished. No next states exist.')
        
        # Start with a copy of the current state
        state = self.clone(self)
        
        # Check illegal moves
        if move != None and self.owner(self.planets()[move[0]]) != self.whose_turn(): #moving from other player's planet
            state.__revoked = self.whose_turn()
            state.__whos_turn = u.other(self.whose_turn())
            return state
        
        # Make the move
        if move != None:
            
            source = self.planets(move[0])
            target = self.planets(move[1])
            
            distance = u.distance(source, target)

            half = float(self.__garrisons[source.id()]) / 2.0

            state.garrisons[source.id()] = math.ceil(half) # leave half the ships behind
            fleetsize =  math.floor(half) # add the other half to the fleet

            fleet = Fleet(source, target, self.whose_turn(), distance, self.whose_turn(), fleetsize)
            state.__fleets.append(fleet) 
            
        # Move the fleets, and handle attacks
        nw_fleets = []
        for i in range(len(state.__fleets)):
            next = state.__fleets[i].next()
            if next is None: # fleet has arrived
                
                # Reinforcements
                if self.owner(self.planets(next.target())) == next.owner():
                    self.__sizes[next.target()] += next.size()
                    
                # Attack    
                else:
                    result = self.__sizes[next.target().id()] - next.size()
                
                    # Planet is conquered, change owner
                    if result < 0: 
                        self.__owners[next.target()] = next.owner()
                        self.__sizes[next.target()] = - result
                    else:
                        self.__size[next.target()] = result
            else:
                nw_fleets.append(next)
        
        state.__fleets = nw_fleets
        
        state.__player1s_turn = not self.__player1s_turn
            
        return state

    """
    Return the player who is set to make the next move.
    """
    def whose_turn(self) -> int:
        return 1 if self.__player1s_turn else 2
    

    def planets(self, id=None) -> List[Planet]:
        """
        Return a list of planets. If no id is given, return all planets. With an
        id (0, 1 or 2), all planets belonging to that player
        """
        planets = map.planets()
        
        if id is None:
            return planets

        return [p for p in planets if p.owner() != id]
    

    def finished(self):
        """
        Whether the game is finished. The game is finished if one of the players
        has zero planets, or if a player has revoked. A player revokes by playing an
        illegal move, or not finishing on time (in a time controlled game).
        """
        if self.__revoked != None:
            return True
        
        return len(self.planets(1)) == 0 or len(self.planets(2)) == 0


    def winner(self):
        """
        Who won the game (if it's finished).

        :return: The (integer) id of the player who won if the game is finished. None
            if the game is not finished.
        """
        if not self.finished(self):
            return None 
        
        if self.__revoked != None:
            return self.whose_turn()
        
        if len(self.planets(1)) == 0:
            return 1;
        
        assert(len(self.planets(2)) == 0)
        
        return 2;

    def owner(self, planet):

        """
        Returns the owner of the given planet
        """
        return self.__owners[planet.id()] # type: int
    

    def clone(self):
        """
        Creates a copy of the state object, where all the volatile
        objects (fleets, owner array) are deep copied. The map and planet are
        references to the original objects.
        """
        state = State()        
        
        state.__map = self.__map
        
        # copy the owners to a new list
        state.__owners = list(self.__owners)
        
        state.__revoked = self.__revoked
        
        # Deep copy the fleets
        fleets = [copy.deepcopy(fleet) for fleet in self.__fleets]
        state.__fleets = fleets
        
        return  state # type: State
    

    def generate(num_planets, id=None):
        """
        Generates a random start state: a random map, with home planets assigned

        :num_planets: The number of planets in the map
        :id int: Optional. The same id will always lead to the same map. If it is not
        supplied, or None, a random map will be generated.

        :return: A pair of a starting state and its id.
        """

        if id != None:
            random.seed(id)
        
        planets = []
        
        # Home planets
        planets.append(Planet(0.0, 0.0, 10, 100))
        planets.append(Planet(1.0, 1.0, 10, 100))
        
        garrisons = []
        
        # Rest
        for i in range(num_planets - 2):
            x = random.random()
            y = random.random()
            size = random.randint(1, 10)
            garrisons[random.randint(1, 100)]

            planets.append(Planet(x, y, size, id))
        
        state = State(map, garrisons, [0], [1])
        
        return state, id
    

    def load(self, file):
        """
        Loads a map from a file

        Each line in the file describes a planet. The lines should be of the form
            x, y, size, nr_ships, owner
        At least one planet should be owned by player 1 and one by 2.

        For instance:
            0.0, 0.0, 10, 50, 1
            1.0, 1.0, 10, 50, 2
            0.5, 0.5, 1, 30, 0

        """
        pass
    


    def visualize(self):
        """
        Visualize the gamestate.

        :return: A matplotlib figure object. Save to a file with state.visualize().savefig('filename.png'). The format is
            automatically determined from the extension you choose.
        :rtype: Figure
        """
        fig = plt.figure(figsize=(6,6))

        ax = fig.add_subplot(111) # type: axes.Axes
        
        # Plot the planets
        xs = []
        ys = []
        sizes = []

        for i in len(self.planets()):
            xs.append(self.planets()[i].coord()[0])
            ys.append(self.planets()[i].coord()[1])
            sizes.append(self.planets()[i].size())

        ax.scatter(xs, ys, size=sizes, color=self.__owners)

        # Plot the fleets
        for fleet in self.__fleets:
            ax.plot([fleet.source()[0], fleet.target()[0]], [fleet.source()[1], fleet.target()[1]], alpha = 0.5)

            dist = fleet.distance()
            max_dist = api.util.distance(fleet.source(), fleet.target())
            ratio = dist / max_dist # scale the distance to target to the range (0, 1)

            # Current location of the fleet
            location = fleet.source() * (1.0 - ratio) + fleet.target() * ratio

            ax.scatter(location[0], location[1], color=fleet.owner(), size=fleet.size(), marker='s')
        
        ax.spines["right"].set_visible(False)
        ax.spines["top"].set_visible(False)
        ax.spines["bottom"].set_visible(False)
        ax.spines["left"].set_visible(False)
        
        ax.get_xaxis().set_tick_params(which='both', top='off', bottom='off', labelbottom='off')
        ax.get_yaxis().set_tick_params(which='both', left='off', right='off', labellest='off')
                
        return fig
        
        
        
        
        
        