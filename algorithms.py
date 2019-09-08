import numpy as np
import random
from abc import abstractmethod
import collections

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
    def _make_action(self, state):
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

    def __init__(self, environment, epsilon, beta, gamma, alpha):
        super().__init__(environment, epsilon, beta, gamma, alpha)
        self._V = []
        self._mi = []

    # def __reset(self):
    #     self.V = np.ones(self._env.size_vertical, self._env.size_horizontal)
    #     self.mi = np.zeros(self._env.size_vertical, self._env.size_horizontal, len(self._actions))

    def _make_action(self, state):
        A = self._env.actions
        greedy_action = []
        max_mi = max(self._mi[state][:])
        for x in range(len(self._actions)):
            if self._mi[state][x] == max_mi:
                # +1 because A = [1,2,3,4] and x <0,3>
                greedy_action.append(x + 1)
        if random() < self._epsilon:
            action = A[randint(0, (len(greedy_action) - 1))]
        else:
            action = greedy_action[randint(0, (len(greedy_action) - 1))]

        return action, self._env.make_move(action, state)

    def learn(self, size_episodes, size_measurement):
        for measurement in range(size_measurement):
            self._V = np.ones(self._env.size_state)
            self._mi = np.zeros((self._env.size_state, len(self._actions)))
            self.data = np.empty((size_episodes, size_measurement))

            for episode in range(size_episodes):

                current_state = self._env.reset()
                self._rout = []
                print(episode)

                while True:
                    previous_state = current_state
                    print(current_state)

                    action, current_state = self._make_action(current_state)
                    self._rout.append(action)
                    print(action)

                    prize = self._env.get_Prize(current_state)

                    delta = prize + self._gamma * self._V[current_state] - self._V[previous_state]
                    self._V[previous_state] = self._alpha * delta
                    self._mi[previous_state][action - 1] += self._beta * delta


                    if self._env.is_absorbing_state(self._rout, current_state):

                        self.data[episode][measurement] = len(self._rout)
                        break


class AHClambda(Algorithm):

    def __init__(self, grid_environment,  epsilon, beta, gamma, alpha, lambd):
        super().__init__(grid_environment, epsilon, beta, gamma, alpha, lambd)
        # todo: description of fields
        self._V = []
        self._mi = []
        self._e = []
        self._ea = []

    def _make_action(self, state):
        A = self._env.actions
        greedy_action = []
        max_mi = max(self._mi[state][:])
        for x in range(len(self._actions)):
            if self._mi[state][x] == max_mi:
                # +1 because A = [1,2,3,4] and x <0,3>
                greedy_action.append(x + 1)
        if random() < self._epsilon:
            action = A[randint(0, (len(greedy_action) - 1))]
        else:
            action = greedy_action[randint(0, (len(greedy_action) - 1))]

        return (action, self._env.make_move(action, state))

    def learn(self, size_episodes, size_measurement):
        for measurement in range(size_measurement):
            self._V = np.ones(self._env.size_state)
            self._mi = np.zeros((self._env.size_state, len(self._actions)))
            self._e = np.zeros(self._env.size_state)
            self._ea = np.zeros((self._env.size_state, len(self._actions)))
            self.data = np.empty((size_episodes, size_measurement))


            for episode in range(size_episodes):

                current_state = self._env.reset()
                self._rout = []

                while True:
                    previous_state = current_state
#todo new indets from atom, spradzic lambde
                    for x in range(self._env.size_state):
                        if x == current_state:
                            self._e[x] +=1
                            continue
                        self._e[x] *= self._gamma * self._lambda

                    action, current_state = self._make_action(current_state)
                    self._rout.append(action)

                    prize = self._env.get_Prize(current_state)

                    for x in range(self._env.size_state):
                        for a in range(len(self._env.actions)):
                            if (x, a) == (current_state, action):
                                self._ea[x][a] += 1
                                continue
                            self._ea[x][a] *= self._gamma * self._lambda


                    delta = prize + self._gamma * self._V[current_state] - self._V[previous_state]
                    self._V[previous_state] += self._alpha * delta *self._e[current_state]
                    self._mi[previous_state][action - 1] += self._beta * delta * self._ea[current_state][action - 1]

                    if self._env.is_absorbing_state( self._rout, current_state):
                        self.data[episode][measurement] = len(self._rout)
                        break

class Qlearning(Algorithm):

    def __init__(self, grid_environment,  epsilon, beta, gamma, alpha):
        super().__init__(grid_environment, epsilon, beta, gamma, alpha)
        self._Q = []

    def _make_action(self, state):
        A = self._env.actions
        greedy_action = []
        max_Q = max(self._Q[state][:])
        for x in range(len(self._actions)):
            if self._Q[state][x] == max_Q:
                # +1 because A = [1,2,3,4] and x <0,3>
                greedy_action.append(x + 1)
        if random() < self._epsilon:
            action = A[randint(0, (len(greedy_action) - 1))]
        else:
            action = greedy_action[randint(0, (len(greedy_action) - 1))]

        return action, self._env.make_move(action, state)


    def learn(self, size_episodes, size_measurement):
        for measurement in range(size_measurement):
            self._Q = np.zeros((self._env.size_state, len(self._actions)))

            for episode in range(size_episodes):
                current_state = self._env.state
                self._rout = []

                while True:
                    previous_state = current_state
                    action, current_state = self._make_action(current_state)
                    self._rout.append(action)

                    prize = self._env.get_Prize(current_state)

                    maxQ_ = max(Q[current_state][:])
                    delta = prize + self._gamma * maxQ_ - self._Q[previous_state][action - 1]

                    self._Q[previous_state][action - 1] +=self._alpha * delta

                    if self._env.is_absorbing_state(self._rout, current_state):
                        self.data[episode][measurement] = len(self._rout)
                        break


class QlearningLambda(Algorithm):
    def __init__(self, grid_environment,  epsilon, beta, gamma, alpha):
        super().__init__(grid_environment, epsilon, beta, gamma, alpha)
        self._Q = []
        self._e = []

    def _make_action(self, state):
        A = self._env.actions
        greedy_action = []
        max_Q = max(self._Q[state][:])
        for x in range(len(self._actions)):
            if self._Q[state][x] == max_Q:
                # +1 because A = [1,2,3,4] and x <0,3>
                greedy_action.append(x + 1)
        if random() < self._epsilon:
            action = A[randint(0, (len(greedy_action) - 1))]
        else:
            action = greedy_action[randint(0, (len(greedy_action) - 1))]

        return action, self._env.make_move(action, state)


    def learn(self, size_episodes, size_measurement):
        for measurement in range(size_measurement):
            self._Q = np.zeros((self._env.size_state, len(self._actions)))
            self._e = np.zeros((self._env.size_state, len(self._actions)))

            for episode in range(size_episodes):
                current_state = self._env.state
                self._rout = []

                while True:
                    previous_state = current_state
                    action, current_state = self._make_action(current_state)
                    self._rout.append(action)

                    prize = self._env.get_Prize(current_state)

                    for x in range(self._env.size_state):
                        for a in range(len(self._env.actions)):
                            if (x, a) == (current_state, action):
                                self._e[x][a] += 1
                                continue
                            self._e[x][a] *= self._gamma * self._lambda

                    maxQ_ = max(Q[current_state][:])
                    delta = prize + self._gamma * maxQ_ - self._Q[previous_state][action - 1]

                    self._Q[previous_state][action - 1] += self._alpha * delta \
                                                            * self._e[previous_state][action - 1]

                    if self._env.is_absorbing_state(self._rout, current_state):
                        self.data[episode][measurement] = len(self._rout)
                        break


class R (Algorithm):
    def __init__(self, grid_environment,  epsilon, beta, gamma, alpha):
        super().__init__(grid_environment, epsilon, beta, gamma, alpha)
        self._Q = []
        self.ro = 0

    def _make_action(self, state):
        A = self._env.actions
        greedy_action = []
        max_Q = max(self._Q[state][:])
        for x in range(len(self._actions)):
            if self._Q[state][x] == max_Q:
                # +1 because A = [1,2,3,4] and x <0,3>
                greedy_action.append(x + 1)
        if random() < self._epsilon:
            action = A[randint(0, (len(greedy_action) - 1))]
        else:
            action = greedy_action[randint(0, (len(greedy_action) - 1))]

        return action, self._env.make_move(action, state)

    def learn(self, size_episodes, size_measurement):
        for measurement in range(size_measurement):
            self._Q = np.zeros((self._env.size_state, len(self._actions)))

            for episode in range(size_episodes):
                current_state = self._env.state
                self._rout = []

                while True:
                    previous_state = current_state
                    action, current_state = self._make_action(current_state)
                    self._rout.append(action)

                    prize = self._env.get_Prize(current_state)
                    maxQ_ = max(Q[current_state][:])
                    maxQ = max(Q[previousPositionX][previousPositionY][:])
                    value_Q_previous = Q[previousPositionX][previousPositionY][action - 1]
                    delta = prize - ro + gamma * maxQ_ - value_Q_previous

                    Q[previousPositionX][previousPositionY][action - 1] += alpha*delta

                    if Q[previousPositionX][previousPositionY][action - 1] == maxQ:
                        ro += beta * (prize - ro + maxQ_ - maxQ)

                    if self._env.is_absorbing_state(self._rout, current_state):
                        self.data[episode][measurement] = len(self._rout)
                        break

class DynaLearning (Algorithm):
    def __init__(self, grid_environment, n,  epsilon, beta, gamma, alpha):
        super().__init__(grid_environment, epsilon, beta, gamma, alpha)
        self.step = collections.namedtuple("Step", field_names=['state','action','next_state','reward'])
        self._Q = []
        self._model = []
        self.memory = []
        self.n = n

    def _make_action(self, state):
            A = self._env.actions
            greedy_action = []
            max_Q = max(self._Q[state][:])
            for x in range(len(self._actions)):
                if self._Q[state][x] == max_Q:
                    # +1 because A = [1,2,3,4] and x <0,3>
                    greedy_action.append(x + 1)
            if random() < self._epsilon:
                action = A[randint(0, (len(greedy_action) - 1))]
            else:
                action = greedy_action[randint(0, (len(greedy_action) - 1))]

            return action, self._env.make_move(action, state)


    def learn(self, size_episodes, size_measurement):
        for measurement in range(size_measurement):
            print(measurement)
            self._Q = np.zeros((self._env.size_state, len(self._actions)))
            #self._model = np.zeros((self._emv.size_state, len(self._actions)))

            for episode in range(size_episodes):
                print(episode)
                current_state = self._env.state
                self._rout = []
                self.cleanBuffer()

                while True:
                    previous_state = current_state
                    action, current_state = self._make_action(current_state)
                    self._rout.append(action)

                    prize = self._env.get_Prize(current_state)

                    #self.addToBuffer(self.step(state=previous_state,action=action,next_state=current_state,reward=prize))
                    self.addToBuffer((previous_state,action,current_state,prize))
                    maxQ_ = max(self._Q[current_state][:])
                    delta = prize + self._gamma * maxQ_ - self._Q[previous_state][action - 1]
                    print(current_state)

                    self._Q[previous_state][action - 1] += self._alpha * delta
                    for x in range(self.n):
                        state, action, next_state, reward = self.sampleFromBuffer()
                        maxQ_ = max(self._Q[next_state][:])
                        delta = reward + self._gamma * maxQ_ - self._Q[state][action-1]
                        self._Q[state][action-1] += self._alpha * delta

    def addToBuffer(self, x):
        self.memory.append(x)

    def sampleFromBuffer(self, batch = 1):
        return random.choice(self.memory)

    def cleanBuffer(self):
        self.memory.clear()
