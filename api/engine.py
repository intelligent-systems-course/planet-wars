"""
This file contains functions to regulate game play.
"""
from matplotlib.backends.backend_pdf import PdfPages
from api import State
import multiprocessing

"""
Play a game between two given players, from the given starting state. 

 
"""
def play(player1, player2, state : State, max_time=5000, verbose=True, outfile='game.pdf'):
    
    print('player1: {}'.format(player1), verbose)
    print('player2: {}'.format(player2), verbose)
    
    # Check if the inputs are correct 
    if state.whos_turn() != 1:
        raise ValueError('The starting state should have player 1 to move')

    pdf = None
    if not outfile is None:
        pdf = PdfPages(outfile)

    # The game loop
    while not state.finished():
        if not pdf is None:
            pdf.savefig(figure=state.visualize())
        
        player = player1 if state.whos_turn() == 1 else player2

        process_result = []
        process = multiprocessing.Process(target=call_player, args=(player, state, result))
        process.start()
        process.join(max_time/1000)

        move = None
        if process.is_alive():
            print('!   Player {} took too long, no move made.'.format(state.whose_turn()))

            process.terminate()
            process.join()

        else:
            move = ...

        print('*   Player {} does: {}'.format(state.whos_turn(), move), verbose)
                
        state = state.next(move)
        
        if state.revoked():
            print('!   Player {} revoked (illegal move), game finished.'.format(state.whose_turn()))
    
    print('Game finished. Player {} has won.'.format(state.winner(), verbose))

    if not pdf is None:
        pdf.close()

def call_player(player, state, result):
    result[0] = player.do_turn(state)

def other(p):
    return 2 if p == 1 else 1

def print(string, verbose):
    if(verbose):
        print(string)