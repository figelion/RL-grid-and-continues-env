from environment_abc import EnvironmentABC
from numpy import pi, sin, cos



class BallBeam(EnvironmentABC):
    g = 9.81

    def __init__(self, position=0.1, angle=- pi / 8, speed=0.1, time_step=0.1, beam_length=1, stop_condition = 1000):
        self.position = position
        self.angle = angle
        self.speed = speed
        self.time_step = time_step
        self.beam_length = beam_length
        self.size_state = 6 * 6
        self.stop_condition = stop_condition
        self.actions = [1, 2, 3, 4, 5]

    def make_move(self, action, environment_parameters):

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

        self.speed += self.time_step*self.g*sin(self.angle)
        self.position += self.time_step*self.speed

        return self.convert_parameters_to_state()

    def is_absorbing_state(self, actions, *args):
        if self.position > 1 : return True
        elif self.position < -1 : return True
        elif len(actions) > self.stop_condition : return True

    def convert_parameters_to_state(self):
        if self.position > 1: state_x = 0
        elif self.position >= 0.5: state_x = 1
        elif self.position >= -0.1: state_x = 2
        elif self.position >= -0.5: state_x = 3
        elif self.position >= -1: state_x = 4
        elif self.position < -1: state_x = 5

        if self.speed > 1: state_y = 0
        elif self.speed >= 0.5: state_y = 1
        elif self.speed >= -0.1: state_y = 2
        elif self.speed >= -0.5: state_y = 3
        elif self.speed >= -1: state_y = 4
        elif self.speed < -1: state_y = 5

        return state_x * 6 + state_y

    def convert_state_to_parameters(self, state):
        pass

    def get_Prize(self, *args):
        if self.position > 1: prize = -1
        elif self.position >= 0.5: prize = 0
        elif self.position >= -0.1: prize = 0
        elif self.position >= -0.5: prize = 0
        elif self.position >= -1: prize = 0
        elif self.position < -1: prize = -1

        return prize

    def reset(self):
        self.position = 0.1
        self.angle = - pi / 8
        self.speed = 0.1

        return self.convert_parameters_to_state()


class CarnOnMountain(EnvironmentABC):
    g=9.81

    def __init__(self, position=0.1, speed=0, time_step=0.1, stop_condition = 1000):
        self.position = position
        self.throttle = speed
        self.time_step = time_step
        self.size_state = 6 * 6
        self.stop_condition = stop_condition
        self.actions = [1, 2, 3]

    def make_move(self, action, environment_parameters):

        if action == 1:
            self.throttle = -1
        elif action == 2:
            self.throttle = 0
        elif action == 3:
            self.throttle = 1

        self.speed += 0.001*self.throttle - 0.0025*cos(3*self.position)
        if self.speed  <=-0.07:
            self.speed = -0.07
        elif self.speed >= 0.07:
            self.speed = 0.07

        self.position += self.speed
        if self.position <= -1.2:
            self.position = -1.2

        return self.convert_parameters_to_state()

    def convert_parameters_to_state(self):

        if self.position <= -1.0: x = 0
        elif self.position <= -0.8: x = 1
        elif self.position <= -0.6: x = 2
        elif self.position <= -0.4: x = 3
        elif self.position <= -0.2: x = 4
        elif self.position <= 0.0: x = 5
        elif self.position <= 0.2: x = 6
        elif self.position <= 0.5: x = 7

        if self.speed <= -0.05: y = 0
        elif self.speed <= -0.03: y = 1
        elif self.speed <= -0.01: y = 2
        elif self.speed <= 0.00: y = 3
        elif self.speed <= 0.01: y = 4
        elif self.speed <= 0.03: y = 5
        elif self.speed <= 0.05: y = 6
        elif self.speed <= 0.07: y = 7

        return x * 8 + y

    def
