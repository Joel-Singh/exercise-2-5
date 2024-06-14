import math
import matplotlib.pyplot as plt
import numpy as np
import random

# Page 31 Second Edition Barto and Sutton
def calculateNewAverageIncrementally(oldAverage, nextValue, numberOfValues):
    return oldAverage + (1/numberOfValues) * (nextValue - oldAverage)

averageRewards = []
levers = [
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    1.0,
]

def randomLever():
    lever = math.floor(random.random() * 10)
    leverReward = levers[lever]
    return {
        "leverIndex": lever,
        "leverReward": leverReward
    }

for i in range(99999):
    if (i == 0):
        averageRewards.append(randomLever()["leverReward"])
    else:
        averageRewards.append(
            calculateNewAverageIncrementally(averageRewards[i - 1], randomLever()["leverReward"], i + 1)
        )
    for lever,reward in enumerate(levers):
        levers[lever] += np.random.normal(0, 0.01)

plt.plot(averageRewards)
plt.ylabel("Average rewards")
plt.xlabel("Step")
plt.show()
