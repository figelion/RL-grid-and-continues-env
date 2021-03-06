import algorithms as alg
from continous_environments import BallBeam
from grid_environments import grid66
from copy import copy
import numpy as np
import matplotlib.pyplot as plt

episode_size = 50
measurement_size = 30

env = copy(grid66)
#env = BallBeam(stop_condition=1000, time_step=0.01)
ahc = alg.DynaLearning(grid_environment=env, n=3, epsilon=0.05, beta=0.5, gamma=0.9, alpha=0.5)
#ahc = alg.Qlearning(grid_environment=env, epsilon=0.05, beta=0.5, gamma=0.9, alpha=0.5)
ahc.learn(episode_size, measurement_size)
print(ahc.data)

std_data = []
avg_data = []
for x in range(episode_size):
    values_row = ahc.data[x][:]
    std_data.append(np.std(values_row))
    avg_data.append(np.average(values_row))

plt.xlabel("Episodes")
plt.ylabel("Actions")
plt.plot(std_data, label="std")
plt.plot(avg_data, label="avg")
plt.legend()
plt.show()
