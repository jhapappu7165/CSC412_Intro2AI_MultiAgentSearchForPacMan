# boardgames.py
# ------------------------------------------------------------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to USM including a link to https://sites.usm.edu/banerjee
#
# This boardgames project was developed at USM by Bikramjit Banerjee. 
# See usage examples below.
#-------------------------------------------------------------------------
import sys
from games4e import GameStateWrapper

def default(str):
    return str + ' [Default: %default]'
def readCommand(argv):
    """
    Processes the command used to run games from the command line.
    """
    from optparse import OptionParser
    usageStr = """
    USAGE:      python boardgames.py <options>
    EXAMPLES:   (1) python boardgames.py
                    - starts an interactive game of TicTacToe with MinimaxAgent and depth=2
                (2) python boardgames.py -t ConnectFour -a AlphaBetaAgent -d 3
                    - game, searchagent, and depth are now set to ConnectFour, AlphaBetaAgent and 3.
    """
    parser = OptionParser(usageStr)

    parser.add_option('-t', '--type', dest='gametype',
                      help=default('the type of GAME to play'), metavar='GAMETYPE', default='TicTacToe')

    parser.add_option('-a', '--agent', dest='agent',
                      help=default(
                          'the agent TYPE in the multiAgents module to use'),
                      metavar='AGENTTYPE', default='MinimaxAgent')
    parser.add_option('-d', '--depth', dest='depth', type='int',
                      help=default('the depth of search'), metavar='DEPTH', default=2)
    options, otherjunk = parser.parse_args(argv)
    if len(otherjunk) != 0:
        raise Exception('Command line input not understood: ' + str(otherjunk))
    return options

options = readCommand(sys.argv[1:])
init_turn = int(input("Who should go first, you (1) or I/computer (0):"))
role = 'X' if init_turn == 0 else 'O'
game = getattr(__import__('games4e'), options.gametype)(computer=role)
ai = getattr(__import__('multiAgents'), options.agent)(depth=options.depth)

state = GameStateWrapper(game, game.initial)
turn = 0
a = (0,0)
while not game.terminal_test(state.cur_state):
    if turn % 2 == init_turn:
        a = ai.getAction(state)
        print("Computer moved",a)
    else:
        game.display(state.cur_state)
        acts = game.actions(state.cur_state)
        if len(acts) == 1:
            a = acts[0]
            print("Your move is",a)
        else:
            while a not in game.actions(state.cur_state):
                inp = input("Your move. Enter valid coords (format: 2,1): ")
                coords = inp.split(',')
                a = (int(coords[0]), int(coords[1]))
    state = state.generateSuccessor(0,a)
    turn += 1

print("===========\nFinal board\n===========")
game.display(state.cur_state)
if state.cur_state.utility == 0:
    print("It's a draw :-|")
elif turn % 2 == init_turn:
    print("You rock!")
else:
    print("You suck!")
    
        
