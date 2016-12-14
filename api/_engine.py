"""
This file contains functions to regulate game play.
"""
from api import *

"""
Play a game between two given players, from the given starting state. 

 
"""
def play(player1, player2, state, verbose=True, visualize=True):
    
    pr('player1: {}'.format(player1), verbose)
    pr('player2: {}'.format(player2), verbose)
    
    # Check if the inputs are correct 
    if state.whos_turn() != 1:
        raise ValueError('The starting state should have player 1 to move')
    
    # The game loop
    while not state.finished():
        if(visualize):
            state.plot('./plie.{}.png')
        
        player = player1 if state.whos_turn() == 1 else player2
        
        move = player1.get_move(state)
        
        pr('    Player {} does: {}'.format(state.whos_turn(), move), verbose)
                
        state = state.next(move)
        
        if state.revoked():
            pr('Player {} made an illegal move, game finished.'.format(state, whos_turn))
             
    
    pr('Game finished. Player {} has won.'.format(state.winner(), verbose))
    
def other(p):
    return 2 if p == 1 else 1

def log(string, verbose):
    if(verbose):
        pr(string)