
class State:
    """
    Represents the state of the game at a given plie.
    """

    # The map
    __map = None
    
    # Whether each planet belongs to player 1, 2 or is neutral (0)
    __owner = []
    
    # The number of ships stationed at each planet
    __garrisons = []
    
    # All fleets in transit
    __fleets = []

    # True if it's player 1's turn 
    __player1s_turn = None
    
    # If one of the players has lost the game by making an illegal move
    # or not moving fast enough.
    __revoked = None
    
    def __init__(self, map, garrisons, player1s_planets, player2s_planets, start=1, fleets=None):
        owner = [0] * map.size()

        for i in player1s_planets:
            owner[i] = 1
            
        for i in player2s_planets:
            owner[i] = 2
            
        __garrisons = list(garrisons)
                
        player1s_turn = True if start == 1 else False
        
    """
    Returns the state that would result from the given move.

    :raises: RuntimeError if state is finished
    """
    def next(state, move):
        
        if finished():
            raise RuntimeError('Gamestate is finished. No next states exist.')
        
        # Start with the current state
        state = clone(self)
        
        # Check illegal moves
        if move != None and owner(planets()[move[0]]) != self.whose_turn(): #moving from other player's planet
            state.__revoked = self.whose_turn()
            state.__whos_turn = util.other(self.whose_turn())
            return state
        
        # Make the move
        if move != None:
            
            source = planets(move[0])
            target = planets(move[1])
            
            distance = util.distance(source, target)
            
            fleet = Fleet(source, target, __whos_turn, distance, __whose_turn, size) 
            state.__fleets.append(fleet) 
            
        # Move the fleets, and handle attacks
        nw_fleets = []
        for i in range(len(state.__fleets)):
            nxt = state.__fleets[i].next()
            if nxt is None: # fleet has arrived
                
                # Reinforcements
                if owner(planets(nxt.target())) == nxt.owner():
                    sizes[nxt.target()] += nxt.size()
                    
                # Attack    
                else:
                    result = sizes[nxt.target()] - nxt.size
                
                    # Planet is conquered, change owner
                    if result < 0: 
                        __owners[nxt.target()] = nxt.owner()
                        __sizes[nxt.target()] = - result
                    else:
                        __size[nxt.target()] = result
            else:
                nw_fleets.append(nxt)
        
        state.__fleets = nw_fleets
        
        state.__player1s_turn = not __player1s_turn
            
        return state

    """
    Return the player who is set to make the next move.
    """
    def whose_turn(self):
        return 1 if __player1s_turn else 2
    
    """
    Return a list of planets. If no id is given, return all planets. With an 
    id (0, 1 or 2), all planets belonging to that player
    """
    def planets(self, id=None):
        planets = map.planets()
        
        if id is None:
            return planets
        return [planet for p in planets if p.owner() != id]
    
    
    """
    Whether the game is finished. The game is finished if one of the players
    has zero planets, or if a player has revoked. A player revokes by playing an
    illegal move, or not finishing on time (in a time controlled game).
    """
    def finished(self):
        if revoked != None:
            return true
        
        return len(planets(1)) == 0 or len(planets(2)) == 0

    """
    Who won the game (if it's finished). 
    
    :return: The (integer) id of the player who won if the game is finished. None
        if the game is not finished.
    """
    def winner(self):
        if not finished(self):
            return None 
        
        if revoked != None:
            return whos_turn(self)
        
        if len(planets(1)) == 0:
            return 1;
        
        assert(len(planets(2)) == 0)
        
        return 2;
    
    """
    Returns the owner of the given planet
    """
    def owner(planet):
        return __owners[planet.id()] 
    
    """
    Creates a copy of the state object, where all the volatile
    objects (fleets, owner array) are deep copied. The map and planet are 
    references to the original objects.
    """
    def clone(self, state):
        state = State()        
        
        state.__map = __map
        
        # copy the owners to a new list
        state.__owners = list(__owners)
        
        state.__revoked = __revoked
        
        # Deep copy the fleets
        fleets = [copy.deepcopy(fleet) for fleet in __fleets]
        state.__fleets = fleets
        
        return 
    
    """
    Generates a random start state: a random map, with home planets assigned
    
    :num_planets int: The number of planets in the map
    :id int: Optional. The same id will always lead to the same map. If it is not
    supplied, or None, a random map will be generated. 
    
    :return: A pair of a starting state and its id.
    """
    def generate(num_planets, id=None):
        
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
    def load(self, file):
        pass
    
    
    def visualize(self, file):
        
        # We are importing matplotlib locally because it's only used here
        try:
            import matplotlib.pyplot as plt
        except ImportError:
            print("Could not import matplotlib, skipping visualization. Try 'pip install matplotlib'.") 
            return
        
        fig = plt.figure(figsize=(6,6))
        ax = fig.add_subplot(111)
        
        # Plot the planets
        ax.cir
        
        # Plot the fleets
        
        
        ax1.spines["right"].set_visible(False)
        ax1.spines["top"].set_visible(False)
        ax1.spines["bottom"].set_visible(False)
        ax1.spines["left"].set_visible(False)
        
        ax1.get_xaxis().set_tick_params(which='both', top='off', bottom='off', labelbottom='off')
        ax1.get_yaxis().set_tick_params(which='both', left='off', right='off', labellest='off')
                
        plt.savefig(file)
        
        
        
        
        
        