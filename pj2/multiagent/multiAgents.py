# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for 
# educational purposes provided that (1) you do not distribute or publish 
# solutions, (2) you retain this notice, and (3) you provide clear 
# attribution to UC Berkeley, including a link to 
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero 
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and 
# Pieter Abbeel (pabbeel@cs.berkeley.edu).
#
# Modified by Eugene Agichtein for CS325 Sp 2014 (eugene@mathcs.emory.edu)
#

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
        some Directions.X for some X in the set {North, South, West, East, Stop}
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
        Note that the successor game state includes updates such as available food,
        e.g., would *not* include the food eaten at the successor state's pacman position
        as that food is no longer remaining.
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        currentFood = currentGameState.getFood() #food available from current state
        newFood = successorGameState.getFood() #food available from successor state (excludes food@successor) 
        currentCapsules=currentGameState.getCapsules() #power pellets/capsules available from current state
        newCapsules=successorGameState.getCapsules() #capsules available from successor (excludes capsules@successor)
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        score = successorGameState.getScore()
        food_min = float('inf')
        ghost_min = float('inf')
        cur_food = currentFood.asList()
        new_food = newFood.asList()
        if len(new_food) == 0:
            return float('inf')

        for food in new_food:
            food_min = min(util.manhattanDistance(newPos, food), food_min)

        for ghost in newGhostStates:
            ghost_min = min(util.manhattanDistance(newPos, ghost.getPosition()), ghost_min)

        score += ghost_min / food_min

        return score

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
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        decision = Directions.STOP
        v = -(float('inf'))
        for action in gameState.getLegalActions(0):
            temp = self.min_value(gameState.generateSuccessor(0, action), 1, 0)
            if v < temp:
                v = temp
                decision = action
        return decision

    def max_value(self, state, depth):
        if state.isWin() or state.isLose() or depth == self.depth:
            return self.evaluationFunction(state)
        v = -(float('inf'))
        for action in state.getLegalActions(0):
            v = max(v, self.min_value(state.generateSuccessor(0, action), 1, depth))
        return v

    def min_value(self, state, agentIndex, depth):
        if state.isWin() or state.isLose() or depth == self.depth:
            return self.evaluationFunction(state)
        v = float('inf')
        for action in state.getLegalActions(agentIndex):
            successor = state.generateSuccessor(agentIndex, action)
            if agentIndex == state.getNumAgents() - 1:
                v_temp = self.max_value(successor, depth + 1)
            else:
                v_temp = self.min_value(successor, agentIndex + 1, depth)
            v = min(v, v_temp)
        return v

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        decision = Directions.STOP
        v = -(float('inf'))
        alpha = -(float('inf'))
        beta = float('inf')
        for action in gameState.getLegalActions(0):
            temp = self.min_value(gameState.generateSuccessor(0, action), alpha, beta, 1, 0)
            if v < temp:
                v = temp
                decision = action
            if v > beta:
                return decision
            alpha = max(alpha, v)
        return decision

    def max_value(self, state, alpha, beta, depth):
        if state.isWin() or state.isLose() or depth == self.depth:
            return self.evaluationFunction(state)
        v = -(float('inf'))
        for action in state.getLegalActions(0):
            v = max(v, self.min_value(state.generateSuccessor(0, action), alpha, beta, 1, depth))
            if v > beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(self, state, alpha, beta, agentIndex, depth):
        if state.isWin() or state.isLose() or depth == self.depth:
            return self.evaluationFunction(state)
        v = float('inf')
        for action in state.getLegalActions(agentIndex):
            successor = state.generateSuccessor(agentIndex, action)
            if agentIndex == state.getNumAgents() - 1:
                v_temp = self.max_value(successor, alpha, beta, depth + 1)
            else:
                v_temp = self.min_value(successor, alpha, beta, agentIndex + 1, depth)
            v = min(v, v_temp)
            if v < alpha:
                return v
            beta = min(beta, v)
        return v

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        decision = Directions.STOP
        v = -(float('inf'))
        for action in gameState.getLegalActions(0):
            temp = self.expect_value(gameState.generateSuccessor(0, action), 1, 0)
            if v < temp:
                v = temp
                decision = action
        return decision

    def max_value(self, state, depth):
        if state.isWin() or state.isLose() or depth == self.depth:
            return self.evaluationFunction(state)
        v = -(float('inf'))
        for action in state.getLegalActions(0):
            v = max(v, self.expect_value(state.generateSuccessor(0, action), 1, depth))
        return v

    def expect_value(self, state, agentIndex, depth):
        if state.isWin() or state.isLose() or depth == self.depth:
            return self.evaluationFunction(state)
        v = 0
        legalActions = state.getLegalActions(agentIndex)
        for action in legalActions:
            successor = state.generateSuccessor(agentIndex, action)
            if agentIndex == state.getNumAgents() - 1:
                v += self.max_value(successor, depth + 1)
            else:
                v += self.expect_value(successor, agentIndex + 1, depth)
        return v / len(legalActions)

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
      Calculate the distance to the closest food and ghost. If the distance to the ghost is within 2 units, pacman will
      run like hell because I directly return the negative infinity. We don't care about the ghosts if they are more
      than 2 units away. If the ghost is scare, I make the score 1.5 times higher so that pacman will be more willing
      to eat capsules. Because the closer to food and less the food the better, I subtract them from the current score.
      I multiply the number of food by 10 so that pacman will do anything to eat food.
    """
    "*** YOUR CODE HERE ***"
    score = currentGameState.getScore()
    currentFood = currentGameState.getFood()  # food available from current state
    currentCapsules = currentGameState.getCapsules()  # power pellets/capsules available from current state
    currentPosition = currentGameState.getPacmanPosition()

    food_min = float('inf')
    ghost_min = float('inf')

    cur_food = currentFood.asList()
    if len(cur_food) == 0:
        return float('inf')

    for food in cur_food:
        food_min = min(util.manhattanDistance(currentPosition, food), food_min)

    for ghostState in currentGameState.getGhostStates():
        ghost_min = min(util.manhattanDistance(currentPosition, ghostState.getPosition()), ghost_min)
        if ghost_min < 2:
            return -float('inf')
        if ghostState.scaredTimer > 0:
            score *= 1.5

    score = score - food_min - 10 * len(cur_food) - len(currentCapsules)
    return score

# Abbreviation
better = betterEvaluationFunction

class ContestAgent(MultiAgentSearchAgent):
    """
      Your agent for the mini-contest
    """

    def getAction(self, gameState):
        """
          Returns an action.  You can use any method you want and search to any depth you want.
          Just remember that the mini-contest is timed, so you have to trade off speed and computation.

          Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
          just make a beeline straight towards Pacman (or away from him if they're scared!)
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

