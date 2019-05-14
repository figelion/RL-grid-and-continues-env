from abc import ABC, abstractmethod


class EnvironmentABC(ABC):

    @abstractmethod
    def make_move(self, action, environment_parameters):
        """
        Take an action for the current state and change environment state

        :param action: previously picked action by a strategy
        :param environment_parameters:
        :return: (action, parameters_decriping_the_agent )
        """
        pass

    @abstractmethod
    def is_absorbing_state(self, environment_parameters, stop_condition):
        """
        Checking if agent have met the absorbing state. In which one the process of learning
        should be terminated or continued in next episode

        :param environment_parameters: parameters which will describe the state of environment
        :param stop_condition: argument which determines the stop condition for the proces of learning.
                              Usually it is number of steps or time for the environments type "to loose"
        :return: bool
        """
        pass

    @abstractmethod
    def convert_parameters_to_state(self, environment_parameters):
        """
        Convert parameters which describe the environment to single integer

        :param environment_parameters: parameters which will describe the state of environment
        :return: int
        """
        pass

    @abstractmethod
    def get_Prize(self, state):
        pass

