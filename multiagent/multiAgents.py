# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        return successorGameState.getScore()

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 1)
    """

    def getAction(self, gameState):
        def minimax(state, agentIndex, depth):
            if depth == 0 or state.isWin() or state.isLose():
                return self.evaluationFunction(state), Directions.STOP

            actions = state.getLegalActions(agentIndex)
            if not actions:
                return self.evaluationFunction(state), Directions.STOP

            numAgents = state.getNumAgents()
            nextAgent = (agentIndex + 1) % numAgents
            nextDepth = depth - 1 if nextAgent == 0 else depth

            if agentIndex == 0: 
                bestVal, bestAct = float("-inf"), Directions.STOP

                for a in actions:
                    succ = state.generateSuccessor(agentIndex, a)
                    val, _ = minimax(succ, nextAgent, nextDepth)
                    if val > bestVal:
                        bestVal, bestAct = val, a

                return bestVal, bestAct

            else:       
                bestVal, bestAct = float("inf"), Directions.STOP

                for a in actions:
                    succ = state.generateSuccessor(agentIndex, a)
                    val, _ = minimax(succ, nextAgent, nextDepth)

                    if val < bestVal:
                        bestVal, bestAct = val, a

                return bestVal, bestAct

        value, action = minimax(gameState, agentIndex=0, depth=self.depth)
        print(value) 
        return action


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 2)
    """

    def getAction(self, gameState):

        def alphabeta(state, agentIndex, depth, alpha, beta):
            if depth == 0 or state.isWin() or state.isLose():
                return self.evaluationFunction(state), Directions.STOP

            actions = state.getLegalActions(agentIndex)

            if not actions:
                return self.evaluationFunction(state), Directions.STOP

            numAgents = state.getNumAgents()
            nextAgent = (agentIndex + 1) % numAgents
            nextDepth = depth - 1 if nextAgent == 0 else depth

            if agentIndex == 0:
                bestVal, bestAct = float("-inf"), Directions.STOP

                for a in actions:
                    succ = state.generateSuccessor(agentIndex, a)
                    val, _ = alphabeta(succ, nextAgent, nextDepth, alpha, beta)

                    if val > bestVal:
                        bestVal, bestAct = val, a

                    if bestVal >= beta:
                        return bestVal, bestAct  # prune
                    alpha = max(alpha, bestVal)
                return bestVal, bestAct

            else:             
                bestVal, bestAct = float("inf"), Directions.STOP

                for a in actions:
                    succ = state.generateSuccessor(agentIndex, a)
                    val, _ = alphabeta(succ, nextAgent, nextDepth, alpha, beta)

                    if val < bestVal:
                        bestVal, bestAct = val, a

                    if bestVal <= alpha:
                        return bestVal, bestAct  # prune

                    beta = min(beta, bestVal)
                return bestVal, bestAct

        value, action = alphabeta(
            gameState, agentIndex=0, depth=self.depth,
            alpha=float("-inf"), beta=float("inf")
        )

        print(value)
        return action




class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 3)
    """

    def getAction(self, gameState):
        def expectimax(state, agentIndex, depth):

            if depth == 0 or state.isWin() or state.isLose():
                return self.evaluationFunction(state), Directions.STOP

            actions = state.getLegalActions(agentIndex)

            if not actions:
                return self.evaluationFunction(state), Directions.STOP

            numAgents = state.getNumAgents()
            nextAgent = (agentIndex + 1) % numAgents
            nextDepth = depth - 1 if nextAgent == 0 else depth

            if agentIndex == 0: 
                bestVal, bestAct = float("-inf"), Directions.STOP

                for a in actions:
                    succ = state.generateSuccessor(agentIndex, a)
                    val, _ = expectimax(succ, nextAgent, nextDepth)

                    if val > bestVal:
                        bestVal, bestAct = val, a

                return bestVal, bestAct

            else:                # CHANCE (uniform over actions)
                prob = 1.0 / float(len(actions))
                expVal = 0.0

                for a in actions:
                    succ = state.generateSuccessor(agentIndex, a)
                    val, _ = expectimax(succ, nextAgent, nextDepth)
                    expVal += prob * val

                return expVal, Directions.STOP

        value, action = expectimax(gameState, agentIndex=0, depth=self.depth)
        print(value)  
        return action



def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOU DON'T NEED TO DO THIS ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction