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
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        #newGhostStates = successorGameState.getGhostStates()
        #newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"

        score = 0 # start with score 0

        foodDistances = [manhattanDistance(newPos, food) for food in newFood.asList()]        # calculate manhattan distance between Pacman and all food dots
        if foodDistances:                                                              #add 100/the shortest distance between pacman and any food dot to the score 
            shortestDistance = min(foodDistances)
            score += 100/shortestDistance

        oldFood = currentGameState.getFood().asList()                 # if Pacman eats food, offer bonus points
        if(newPos in oldFood):
            score += 500

        newGhostPositions = successorGameState.getGhostPositions()    # learn the positions of ghosts

        if(newPos in newGhostPositions):        # if Pacman runs into Ghost in the next step, avoid at all cost!
              score += -10000
              return score

        oldPos = currentGameState.getPacmanPosition()           # subtract points if pacman stays inactive
        if (newPos == oldPos):
            score += -500

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

        def MaxValue(self, gameState, depth):

            actions = gameState.getLegalActions(0) # 0 = Pacman
            if not actions:
                return self.evaluationFunction(gameState)       # if no actions are available, turn ends

            v = float("-inf")
            move = 0

            for action in actions:
               v1 = MinValue(self, gameState.generateSuccessor(0, action), depth, 1) # 1 = First Ghost
               if( v1 > v):
                   v = v1
                   move = action

            if(depth == 0): # final(root) decision --> action to take
                return move
            else:
                return v

        def MinValue(self, gameState, depth, GhostNo):

            actions = gameState.getLegalActions(GhostNo)        #get legal actions of the ghost with this index
            if not actions:
                return self.evaluationFunction(gameState)       #if no actions are available, turn ends

            if (GhostNo == gameState.getNumAgents() - 1):       # if this is the last ghost
                next_agent = 0 # Pacman                         # Pacman's turn is next
            else:
                next_agent = GhostNo + 1

            v = float("inf")

            for action in actions:
                if(next_agent == 0):
                    if(depth == self.depth -1):   # if we're on a leaf, return evaluationFunction result
                        v1 = self.evaluationFunction(gameState.generateSuccessor(GhostNo, action))
                    else:                       # else, start process from MAX = Pacman
                        v1 = MaxValue(self, gameState.generateSuccessor(GhostNo, action), depth + 1)
                else:                               # if next_agent is a ghost, return MinValue for that ghost
                    v1 = MinValue(self, gameState.generateSuccessor(GhostNo, action), depth, next_agent)
                if(v1 < v):
                    v = v1
            return v

        return MaxValue(self, gameState, 0)         #first call of function

        #util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        def MaxValue(self, gameState, depth, a, b):
    
            actions = gameState.getLegalActions(0)
            if not actions:
                return self.evaluationFunction(gameState)

            v = float("-inf")
            move = 0

            for action in actions:
                v1 = MinValue(self, gameState.generateSuccessor(0, action), depth, 1, a, b) # 1 = First Ghost
                if( v1 > v):            # if the new value is greater than the last one
                   v = v1               # old value-->new value
                   move = action        # old move-->new move
                a = max(a, v)           # best choice for MAX so far is the max between the current best choice and the new value
                if(v > b):              # if v is better than current best choice for MIN, return v
                    return v

            if(depth == 0): # final decision --> action to take
                return move
            else:
                return v

        def MinValue(self, gameState, depth, GhostNo, a, b):
        
            actions = gameState.getLegalActions(GhostNo)
            if not actions:
                return self.evaluationFunction(gameState)

            if (GhostNo == gameState.getNumAgents() - 1):
                next_agent = 0 # Pacman
            else:
                next_agent = GhostNo + 1

            v = float("inf")

            for action in actions:
                if(next_agent == 0):
                    if(depth == self.depth -1):   # if we're on a leaf, return evaluationFunction result
                        v1 = self.evaluationFunction(gameState.generateSuccessor(GhostNo, action))
                    else:                           # else, start process from MAX = Pacman
                        v1 = MaxValue(self, gameState.generateSuccessor(GhostNo, action), depth + 1, a, b)
                else:                           # if next_agent is a ghost, return MinValue for that ghost
                    v1 = MinValue(self, gameState.generateSuccessor(GhostNo, action), depth, next_agent, a, b)
                if(v1 < v):                 # if the new value is less than the old value
                    v = v1                  # old value-->new value
                b = min(b, v)              # best choice for MIN so far is the min between current best choice and the new valie
                if(v < a):                  # if v is less than current best MAX choice , return it
                    return v
            return v

        return MaxValue(self, gameState, 0, float("-inf"), float("inf")) #first call to function
    #    util.raiseNotDefined()

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

        def MaxValue(self, gameState, depth):
        
            actions = gameState.getLegalActions(0) # 0 = Pacman
            if not actions:
                return self.evaluationFunction(gameState)

            v = float("-inf")
            move = 0

            for action in actions:
                v1 = ChanceValue(self, gameState.generateSuccessor(0, action), depth, 1) # 1 = First Ghost
                if( v1 > v):
                   v = v1
                   move = action

            if(depth == 0): # final decision --> action to take
                return move
            else:
                return v

        def ChanceValue(self, gameState, depth, GhostNo):
        
            actions = gameState.getLegalActions(GhostNo)
            if not actions:
                return self.evaluationFunction(gameState)

            if (GhostNo == gameState.getNumAgents() - 1):
                next_agent = 0 # Pacman
            else:
                next_agent = GhostNo + 1

            v = 0

            for action in actions:
                if(next_agent == 0):
                    if(depth == self.depth -1):   # if we're on a leaf, return evaluationFunction result
                        v += self.evaluationFunction(gameState.generateSuccessor(GhostNo, action))
                    else:                           # else, start process from MAX = Pacman
                        v += MaxValue(self, gameState.generateSuccessor(GhostNo, action), depth + 1)
                else:                       #if next_agent is a ghost, return ChanceValue for that ghost
                    v += ChanceValue(self, gameState.generateSuccessor(GhostNo, action), depth, next_agent)
            average = float(v) / len(actions)       # calculate average 
            return average

        return MaxValue(self, gameState, 0)         #first call to function
        # util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    # Useful information you can extract from a GameState (pacman.py)
    pacmanPos = currentGameState.getPacmanPosition()
    foodPos = currentGameState.getFood().asList()
    ghostStates = currentGameState.getGhostStates()
    scaredTimes = [ghostState.scaredTimer for ghostState in ghostStates]
    score = 0 # start with score 0
    capsulePos = currentGameState.getCapsules()        # learn the positions of ghosts
    ghostPos = currentGameState.getGhostPositions()    # learn the positions of ghosts

    foodDistances = [manhattanDistance(pacmanPos, food) for food in foodPos]        # calculate manhattan distance between Pacman and all food dots
    
    if foodDistances:
        shortestFoodDistance = min(foodDistances)   # add 10/the shortest distance between Pacman and any food dot to the score
        if(shortestFoodDistance != 0):
            score += 10.0/shortestFoodDistance

    if(0 not in scaredTimes):           # if all ghost in the maze are currently scared
        ghostDistances = [manhattanDistance(pacmanPos, aGhost) for aGhost in ghostPos] # manhattan distance between Pacman and all ghosts
        if ghostDistances:
            shortestGhostDistance = min(ghostDistances) # add 60/the shortest distance between Pacman and any ghost
            if(shortestGhostDistance != 0):
                score += 60.0/shortestGhostDistance
    else:                               # else add 55/shortest distance from capsule so that Pacman tries to scare the ghosts
        capsuleDistances = [manhattanDistance(pacmanPos, capsule) for capsule in capsulePos]
        if capsuleDistances:
            shortestCapsuleDistance = min(capsuleDistances)
            if(shortestCapsuleDistance != 0):
                score += 55.0/shortestCapsuleDistance

    return score + currentGameState.getScore()      # return calculated score + current score so far
    #util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction