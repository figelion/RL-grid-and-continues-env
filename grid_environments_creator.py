import numpy as np

class GridEnviroment:
    """
    Tool for creating grid environments

    """
    def __init__(self,size_horizontal,size_vertical, type, st_con_loose = 100):
        """
        :param type: type of enviorment 'to_win' or 'to_lose'
        :param st_con_loose: number of actions after the learning will stop for 'to_loose' environment
        """
        self.size_vertical = size_vertical
        self.size_horizontal = size_horizontal
        self.environment = [[0 for x in range(self.size_vertical)] for x in range(self.size_horizontal)]
        self.__actions = [1, 2, 3, 4]
        self.__type = type
        self._stop_condition_to_loose = st_con_loose

    @property
    def stop_condition_to_loose(self):
        return self._stop_condition_to_loose

    @stop_condition_to_loose.setter
    def stop_condition_to_loose(self, value):
        self._stop_condition_to_loose = value

    @property
    def actions(self):
        return self.__actions

    @property
    def type(self):
        return self.__type

    @property
    def size_vertical(self):
        return self._size_vertical

    @size_vertical.setter
    def size_vertical(self, value):
        self._size_vertical = value

    @property
    def size_horizontal(self):
        return self._size_horizontal

    @size_horizontal.setter
    def size_horizontal(self, value):
        self._size_horizontal = value

    def __checkIfObstacleFit (self, start_point, length_obstacle, orientation):
        x,y = start_point
        if orientation == 'V' :
            if length_obstacle > 0 and x >= 0 and x + (length_obstacle-1) <= self.size_vertical :
                return True
            elif length_obstacle < 0 and x >= 0 and x - (length_obstacle - 1) >= 0:
                return True
            else:
                return False
        elif orientation == 'H' :
            if length_obstacle > 0 and x >= 0 and y + (length_obstacle - 1) <= self.size_horizontal:
                return True
            elif length_obstacle < 0 and y >= 0 and y - (length_obstacle-1) >= 0 :
                return True
            else:
                return False


    def createObstacleVertical (self,start_point, length_obstacle):
        # length_obstacle - positive values - obstacle is created on the rigth from start_point
        # length_obstacle - negative values - obstacle is created on the left from start_point
        fit = self.__checkIfObstacleFit(start_point = start_point, length_obstacle = length_obstacle, orientation='V')
        if not fit:
            return print("Vertical obstacle doesn't fit")
        x,y = start_point
        if length_obstacle > 0:
            for i in range(abs(length_obstacle)):
                self.environment[x][y] = -2
                x -= 1
        elif length_obstacle < 0:
            for i in range(abs(length_obstacle)):
                self.environment[x][y] = -2
                x += 1
        else :
            print ("Obstacle length: 0")

    def createObstacleHorizontal (self,start_point, length_obstacle):
        """
        :param start_point: point from which creating will start
        :param length_obstacle: positive values - obstacle is created to the up from start_point
                                negative values - obstacle is created to the down from start_point
        """
        # length_obstacle - positive values - obstacle is created to the up from start_point
        # length_obstacle - negative values - obstacle is created to the down from start_point
        fit = self.__checkIfObstacleFit(start_point=start_point, length_obstacle=length_obstacle, orientation='H')
        if not fit:
            return print("Horizontal obstacle doesn't fit")

        x, y = start_point
        if length_obstacle > 0:
            for i in range(length_obstacle):
                self.environment[x][y] = -2
                y += 1
        elif length_obstacle < 0:
            for i in range(abs(length_obstacle)):
                self.environment[x][y] = -2
                y -= 1
        else:
            print("Obstacle length: 0")

    def clearEnvironment(self):
        self.environment = [[0 for x in range(self.size_vertical)] for x in range(self.size_horizontal)]

    def showEnviorment(self):
        print(np.matrix(self.environment))

    def setPrize(self,point,value):
        x,y = point
        self.environment[x][y] = value

    def getPrize(self,x,y):
        return self.environment[x][y]

    def moveUp(self,start_point):
        x,y = start_point
        x -= 1
        if x < 0 or self.getPrize(x,y) == -2:
            x += 1
        return x

    def moveDown(self,start_point):
        x,y = start_point
        x += 1
        if x > (self.size_vertical - 1) or self.getPrize(x,y) == -2:
            x -= 1
        return x

    def moveLeft(self,start_point):
        x,y = start_point
        y -= 1
        if y < 0 or self.getPrize(x,y) == -2:
            y += 1
        return y

    def moveRight(self,start_point):
        x,y = start_point
        y += 1
        if y > (self.size_horizontal - 1) or self.getPrize(x,y) == -2:
            y -= 1
        return y

    def make_move(self, action, currentPositionX, currentPositionY):
        if action == 1 :
            currentPositionX = self.moveUp((currentPositionX,currentPositionY))
        elif action == 2 :
            currentPositionX = self.moveDown((currentPositionX,currentPositionY))
        elif action == 3 :
            currentPositionY = self.moveLeft((currentPositionX,currentPositionY))
        elif action == 4 :
            currentPositionY = self.moveRight((currentPositionX,currentPositionY))
        else :
            print (f"Wrong action number: {action}")

        return action, currentPositionX, currentPositionY

    def is_absorbing_state (self, currentPositionX, currentPositionY, quantity_actions):
        prize = self.getPrize(currentPositionX, currentPositionY)
        if self.__type == "to_win":
            return prize == 1 or prize == 0.5
        elif self.__type == "to_loose":
            return prize == -1 or quantity_actions >= self.stop_condition_to_loose
