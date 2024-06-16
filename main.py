from collections.abc import Callable
import math
from typing import TypedDict
import matplotlib.pyplot as plt
import numpy as np
import random

# Page 31 Second Edition Barto and Sutton
def calculateNewAverageIncrementally(oldAverage, nextValue, numberOfValues):
    return oldAverage + (1/numberOfValues) * (nextValue - oldAverage)

class Lever(TypedDict):
    estimate: None | float
    getReward: Callable[[], float]
    takeRandomWalk: Callable[[], None]
    getTrueValue: Callable[[], float]

def createLever() -> Lever:
    trueValue = np.random.normal(0, 1)
    def takeRandomWalk():
        nonlocal trueValue
        trueValue += np.random.normal(0, 0.01)
    return {
        # Really should just use 0 as the starting value rather than None
        "estimate": None,
        "getReward": lambda: np.random.normal(trueValue, 1),
        "takeRandomWalk": takeRandomWalk,
        "getTrueValue": lambda: trueValue
    }

averageRewards = []
levers = [
    createLever(),
    createLever(),
    createLever(),
    createLever(),
    createLever(),
    createLever(),
    createLever(),
    createLever(),
    createLever(),
    createLever(),
]

def randomLever():
    lever = math.floor(random.random() * 10)
    leverReward = levers[lever]
    return {
        "leverIndex": lever,
        "leverReward": leverReward
    }
def chooseLeverGreedily():
    def getHighestEstimateLevers(list: list[Lever]) -> list[Lever]:
        highestEstimate = 0
        highestEstimateLevers = []
        for _,lever in enumerate(list):
            estimate = lever['estimate'] if lever['estimate'] is not None else 0
            if (estimate > highestEstimate):
                highestEstimateLevers = []
                highestEstimate = estimate
                highestEstimateLevers.append(lever)
            elif(estimate == highestEstimate):
                highestEstimateLevers.append(lever)
        return highestEstimateLevers

    highestEstimateLevers = getHighestEstimateLevers(levers)
    return random.choice(highestEstimateLevers)

for i in range(99999):
    lever = chooseLeverGreedily()
    reward = lever['getReward']()

    if (lever['estimate'] is None):
        lever['estimate'] = reward
    else:
        lever['estimate'] = calculateNewAverageIncrementally(lever['estimate'], reward, i + 1)

    if (i == 0):
        averageRewards.append(reward)
    else:
        averageRewards.append(
            calculateNewAverageIncrementally(averageRewards[i - 1], reward, i + 1)
        )
    for _,lever in enumerate(levers):
        lever["takeRandomWalk"]()

print()
print("Estimates are")
def getRewardEstimates() -> list[float]:
    rewardEstimates = []
    for _,lever in enumerate(levers):
        rewardEstimates.append(lever["estimate"])
    return rewardEstimates
print(getRewardEstimates())
print()

print("Actual levers are")
def getLeversTrueValues() -> list[float]:
    trueValues = []
    for _,lever in enumerate(levers):
        trueValues.append(lever["getTrueValue"]())
    return trueValues
print(getLeversTrueValues())

plt.plot(averageRewards)
plt.ylabel("Average rewards")
plt.xlabel("Step")
plt.show()
