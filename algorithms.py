import numpy as np
from random import random, randint
from abc import abstractmethod


class Algorithm:
    def __init__(self, environment, epsilon, beta, gamma, alpha, lambd=0):
        # todo description of coefficients
        """
        :param grid_environment:
        :param epsilon:
        :param beta:
        :param gamma:
        :param alpha:
        :param lambd:
        """
        self._env = environment
        self._actions = environment.actions
        self._epsilon = epsilon
        self._beta = beta
        self._gamma = gamma
        self._alpha = alpha
        self._lambda = lambd
        self._rout = []
        self.data = []

    @abstractmethod
    def _make_action(self, current_position_x, current_position_y):
        """
        Is used in the method learn() only.
        Using epsilon-greed strategy choose an action.

        :param current_position_x: Current position of agent (row)
        :param current_position_y: Current position of agent (column)
        """

    @abstractmethod
    def learn(self, size_episodes, size_measurement):
        """
        Start process of learning

        :param size_episodes: By how many episodes a process of learning should be continued
        :param size_measurement: How many times a process of learning should be repeated
        """


class Ahc(Algorithm):

    def __init__(self, grid_environment, epsilon, beta, gamma, alpha):
        super().__init__(grid_environment, epsilon, beta, gamma, alpha)
        self.__V = []
        self.__mi = []

    # def __reset(self):
    #     self.V = np.ones(self._env.size_vertical, self._env.size_horizontal)
    #     self.mi = np.zeros(self._env.size_vertical, self._env.size_horizontal, len(self._actions))

    def _make_action(self, state):
        A = self._env.actions
        greedy_action = []
        max_mi = max(self.__mi[state][:])
        for x in range(len(self._actions)):
            if self.__mi[state][x] == max_mi:
                # +1 because A = [1,2,3,4] and x <0,3>
                greedy_action.append(x + 1)
        if random() < self._epsilon:
            action = A[randint(0, (len(greedy_action) - 1))]
        else:
            action = greedy_action[randint(0, (len(greedy_action) - 1))]

        return self._env.make_move(action, state)

    def learn(self, size_episodes, size_measurement):
        for measurement in range(size_measurement):
            self.__V = np.ones(self._env.size_state)
            self.__mi = np.zeros(self._env.size_state, len(self._actions))
            self.data = np.empty((size_episodes, size_measurement))

            for episode in range(size_episodes):

                current_state = self._env.reset()
                self._rout = []

                while True:
                    previous_state = current_state

                    action, current_state = self._make_action(current_state)
                    self._rout.append(action)

                    prize = self._env.getPrize(current_state)

                    delta = prize + self._gamma * self.__V[current_state] \
                            - self.__V[previous_state]
                    self.__V[previous_state] += self._alpha * delta
                    self.__mi[previous_state][action - 1] += self._beta * delta

                    if self._env.is_absorbing_state(current_state, self._rout):
                        self.data[episode][measurement] = len(self._rout)
                        break


class AHClambda(Algorithm):

    def __init__(self, grid_environment,  epsilon, beta, gamma, alpha):
        super().__init__(grid_environment, epsilon, beta, gamma, alpha)
        # todo: description of fields
        self.__V = []
        self.__mi = []
        self.__e = []
        self.__ea = []

    def _make_action(self, state):
        A = self._env.actions
        greedy_action = []
        max_mi = max(self.__mi[state][:])
        for x in range(len(self._actions)):
            if self.__mi[state][x] == max_mi:
                # +1 because A = [1,2,3,4] and x <0,3>
                greedy_action.append(x + 1)
        if random() < self._epsilon:
            action = A[randint(0, (len(greedy_action) - 1))]
        else:
            action = greedy_action[randint(0, (len(greedy_action) - 1))]

        return self._env.make_move(action, state)

    def learn(self, size_episodes, size_measurement):
        for measurement in range(size_measurement):
            self.__V = np.ones((self._env.size_vertical, self._env.size_horizontal))
            self.__mi = np.zeros((self._env.size_vertical, self._env.size_horizontal, len(self._actions)))
            self.data = np.empty((size_episodes, size_measurement))

            for episode in range(size_episodes):

                current_state = self._env.state
                self._rout = []

                while True:
                    previous_state = current_state

                    action, current_state = self._make_action(current_state)
                    self._rout.append(action)

                    prize = self._env.getPrize(current_state)

                    delta = prize + self._gamma * self.__V[current_state] - self.__V[previous_state]
                    self.__V[previous_state] += self._alpha * delta
                    self.__mi[previous_state][action - 1] += self._beta * delta

                    if self._env.is_absorbing_state(current_state, self._rout):
                        self.data[episode][measurement] = len(self._rout)
                        break
