import grid_environments_creator as env
import math
#grid66
grid66 = env.GridEnvironment(6, 6, "to_win", starting_position=(3, 4))
grid66.createObstacleVertical((1, 1), -4)
grid66.createObstacleVertical((1, 4), -4)
grid66.createObstacleHorizontal((4, 3), 1)
grid66.createObstacleHorizontal((1, 2), 1)
grid66.setPrize((0, 5), 1)
grid66.setPrize((5, 5), 0.5)

#grid69
grid69 = env.GridEnvironment(6, 9, "to_win",starting_position=(5, 2))
grid69.createObstacleVertical((1, 2), -3)
grid69.createObstacleVertical((4, 5), 1)
grid69.createObstacleVertical((0, 7), -3)
grid69.setPrize((0, 8), 1)

#grid69.showEnviorment()

#grid1010
# grid1010 = env.GridEnvironment(10, 10, "to_lose")
# for x in range(10):
#     grid1010.setPrize((x, 0), -1)
#     grid1010.setPrize((0, x), -1)
#     grid1010.setPrize((x, 9), -1)
#     grid1010.setPrize((9, x), -1)
#
# #grid1010.showEnviorment()
#
# #grid2436
# grid2436 = env.GridEnvironment(24, 36, "to_win")
#
# grid2436.createObstacleVertical((5, 8), -12)
# grid2436.createObstacleVertical((5, 9), -12)
# grid2436.createObstacleVertical((5, 10), -12)
# #
# grid2436.createObstacleVertical((20, 20), -4)
# grid2436.createObstacleVertical((20, 21), -4)
# grid2436.createObstacleVertical((20, 22), -4)
# #
# grid2436.createObstacleVertical((0, 28), -12)
# grid2436.createObstacleVertical((0, 29), -12)
# grid2436.createObstacleVertical((0, 30), -12)
#
# grid2436.setPrize((0, 35), 1)
#
# #grid2436.showEnviorment()
#
#
# #grid2525
# grid2525 = env.GridEnvironment(25, 25, "to_lose")
#
# for x in range(25):
#     grid2525.setPrize((x,0), -1)
#     grid2525.setPrize((0,x), -1)
#     grid2525.setPrize((x,24), -1)
#     grid2525.setPrize((24,x), -1)

#grid2525.showEnviorment()
