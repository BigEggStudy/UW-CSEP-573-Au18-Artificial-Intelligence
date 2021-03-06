# rtdpAgents.py
# -----------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu). The RTDP question was added by
# Gagan Bansal (bansalg@cs.washington.edu) and Dan Weld (weld@cs.washington.edu).

import random

import mdp, util

from learningAgents import ValueEstimationAgent

class RTDPAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A RTDPAgent takes a Markov decision process
        (see mdp.py) on initialization and runs rtdp
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100, max_iters=100, reverse=False):
        """
          Your value rtdp agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
              mdp.getStartState()

          Other useful functions:
              weighted_choice(choices)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = {}  # note, we use a normal python dictionary for RTDPAgent.

        # Write rtdp code here
        "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()
        for state in self.mdp.getStates():
            if self.mdp.isTerminal(state):
                continue
            x, y = state
            cell = self.mdp.grid[x][y]
            if type(cell) == int or type(cell) == float:
                self.values[state] = int(cell)

        for i in range(self.iterations):
            startState = self.mdp.getStartState()
            state = startState
            step = 0
            if not reverse:
                while not self.mdp.isTerminal(state) and step < max_iters:
                    step += 1

                    action = self.getAction(state)
                    self.updateValue(state, action)
                    state = self.pickNextState(state, action)
            else:
                stack = util.Stack()
                while not self.mdp.isTerminal(state) and step < max_iters:
                    step += 1
                    action = self.getAction(state)
                    stack.push((state, action))
                    state = self.pickNextState(state, action)

                while not stack.isEmpty():
                    state, action = stack.pop()
                    self.updateValue(state, action)

    def pickNextState(self, state, action):
        """
          Return the next stochastically simulated state.
        """
        "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()
        return weighted_choice(self.mdp.getTransitionStatesAndProbs(state, action))

    def updateValue(self, state, action):
        """
          Update the value of given state.
        """
        "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()
        self.values[state] = self.getQValue(state, action)

    def getHeuristicValue(self, state):
        """
          Return the heuristic value of state.
        """
        "*** YOUR CODE HERE ***"
        # your heuristic function here
        # util.raiseNotDefined()
        if self.mdp.isTerminal(state):
            return 0

        x, y = state
        cell = self.mdp.grid[x][y]
        if type(cell) == int or type(cell) == float:
            return 0

        goalState = self.mdp.getGoalState()
        goalReward = self.mdp.getGoalReward()
        return goalReward * (self.discount ** util.manhattanDistance(state, goalState))

    def getValue(self, state):
        """
          Return the current stored value of the state.
          If the state has not been seen yet then return it heuristic value.

          Note the difference between this and the similar method in valueIterationAgents
        """
        value = None
        if state not in self.values:
            value = self.getHeuristicValue(state)
            self.values[state] = value
        return self.values[state]

    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()
        transition = self.mdp.getTransitionStatesAndProbs(state, action)
        return sum([probability * (self.mdp.getReward(state, action, nextState) + self.discount * self.getValue(nextState)) for nextState, probability in transition])

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()
        if self.mdp.isTerminal(state):
            return None

        actions = self.mdp.getPossibleActions(state)
        qValue_action_map = [(self.computeQValueFromValues(state, action), action) for action in actions]
        return max(qValue_action_map, key = lambda item:item[0])[1]

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)


def weighted_choice(choices):
    """
    Return a random element from list of the form: [(choice, weight), ....]
    Credits: http://stackoverflow.com/questions/3679694
    """
    total = sum(w for c, w in choices)
    r = random.uniform(0, total)
    upto = 0
    for c, w in choices:
       if upto + w >= r:
          return c
       upto += w
    assert False, "Shouldn't get here"
