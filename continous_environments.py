from environment_abc import EnvironmentABC
from math import pi


class Ball_beam(EnvironmentABC):
    def __init__(self, position, angle, speed):
        self.position = position
        self.angle = angle
        self.speed = speed

    def make_move(self, action, environment_parameters):
        position, speed = environment_parameters

        if action == 1:
            self.angle = - pi/4.
        elif action == 2:
            self.angle = - pi / 8.
        elif action == 3:
            self.angle = 0
        elif action == 4:
            self.angle = pi / 8.
        elif action == 5:
            self.angle = pi / 4.

    def is_absorbing_state(self, environment_parameters, stop_condition):
        pass

    def convert_parameters_to_state(self, environment_parameters):
        pass

