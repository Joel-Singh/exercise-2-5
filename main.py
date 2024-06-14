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

rewardEstimates: list[None | float] = [
    None, None, None, None, None, None, None, None, None, None
]

def randomLever():
    lever = math.floor(random.random() * 10)
    leverReward = levers[lever]
    return {
        "leverIndex": lever,
        "leverReward": leverReward
    }

def chooseLeverGreedily():
    def getHighestIndices(list: list[float | None]):
        highestNumber = 0
        highestIndices = []
        for i,v in enumerate(list):
            if v is None:
                v = 0
            if (v > highestNumber):
                highestIndices = []
                highestNumber = v
                highestIndices.append(i)
            elif(v == highestNumber):
                highestIndices.append(i)
        return highestIndices

    highestIndices = getHighestIndices(rewardEstimates)
    randomlyChosenIndex = highestIndices[math.floor(len(highestIndices) * random.random())]
    leverReward = levers[randomlyChosenIndex]
    return {
        "leverIndex": randomlyChosenIndex,
        "leverReward": leverReward
    }

leversChosen = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
for i in range(99999):
    lever = chooseLeverGreedily()
    leverIndex: int = lever["leverIndex"]
    leverReward: float = lever["leverReward"]

    leversChosen[leverIndex] += 1

    if (rewardEstimates[leverIndex] is None):
        rewardEstimates[leverIndex] = leverReward
    else:
        calculateNewAverageIncrementally(rewardEstimates[leverIndex], leverReward, i + 1)

    if (i == 0):
        averageRewards.append(leverReward)
    else:
        averageRewards.append(
            calculateNewAverageIncrementally(averageRewards[i - 1], leverReward, i + 1)
        )
    for lever,reward in enumerate(levers):
        levers[lever] += np.random.normal(0, 0.01)

plt.plot(averageRewards)
plt.ylabel("Average rewards")
plt.xlabel("Step")
print("Levers chosen are")
print(leversChosen)
print()
print("Estimates are")
print(rewardEstimates)
print()
print("Actual levers are")
print(levers)
plt.show()
