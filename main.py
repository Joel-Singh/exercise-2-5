from collections.abc import Callable
from typing import Final, TypedDict
import matplotlib.pyplot as plt
import numpy as np
import random

from numpy.lib import math

DEFAULT_ESTIMATE: Final = 0
CHANCE_TO_SELECT_RANDOMLY: Final = 0.1
ARE_LEVERS_WALKING: Final = True

NUMBER_OF_ITERATIONS: Final = 10000

USE_INCREMENTAL_ESTIMATE_CALCULATION = True
STEP_SIZE_PARAMETER = 0.1

# Page 31 Second Edition Barto and Sutton
def calculateNewAverageIncrementally(oldAverage, nextValue, numberOfValues):
    return oldAverage + (1/numberOfValues) * (nextValue - oldAverage)


def calculateNewAverageWithStepSizeParameter(oldAverage, nextValue, stepSizeParameter):
    return oldAverage + (stepSizeParameter) * (nextValue - oldAverage)

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

def getOptimalLever(levers: list[Lever]):
    optimalLever = levers[0]
    for lever in levers:
        if (optimalLever["getTrueValue"]() < lever["getTrueValue"]()):
            optimalLever = lever
    return optimalLever

optimalLever = getOptimalLever(levers)

def chooseLeverRandomly():
    return random.choice(levers)

def chooseLeverGreedily():
    def getHighestEstimateLevers(list: list[Lever]) -> list[Lever]:
        highestEstimate = 0
        highestEstimateLevers = []
        for _,lever in enumerate(list):
            estimate = lever['estimate'] if lever['estimate'] is not None else DEFAULT_ESTIMATE
            if (estimate > highestEstimate):
                highestEstimateLevers = []
                highestEstimate = estimate
                highestEstimateLevers.append(lever)
            elif(estimate == highestEstimate):
                highestEstimateLevers.append(lever)
        return highestEstimateLevers

    highestEstimateLevers = getHighestEstimateLevers(levers)
    return random.choice(highestEstimateLevers)

timesOptimalLeverIsChosen = 0
for i in range(NUMBER_OF_ITERATIONS):
    def printOutPercentage():
        tenPercent = math.floor(NUMBER_OF_ITERATIONS / 10) - 1
        if ((i % tenPercent) == 0):
            print(str((i / tenPercent) * 10) + "% complete")

    def chooseLever():
        if (random.random() < CHANCE_TO_SELECT_RANDOMLY):
            return chooseLeverRandomly()
        else:
            return chooseLeverGreedily()

    def updateEstimate(lever, reward):
        if (lever['estimate'] is None):
            lever['estimate'] = reward
        else:
            if (USE_INCREMENTAL_ESTIMATE_CALCULATION):
                lever['estimate'] = calculateNewAverageIncrementally(lever['estimate'], reward, i + 1)
            else:
                lever['estimate'] = calculateNewAverageWithStepSizeParameter(lever['estimate'], reward, STEP_SIZE_PARAMETER)

    def updateAverageRewards(reward):
        if (i == 0):
            averageRewards.append(reward)
        else:
            averageRewards.append(
                calculateNewAverageIncrementally(averageRewards[i - 1], reward, i + 1)
            )

    def walkLevers():
        if (ARE_LEVERS_WALKING):
            for _,lever in enumerate(levers):
                lever["takeRandomWalk"]()

    printOutPercentage()

    lever = chooseLever()
    reward = lever['getReward']()

    if (lever is optimalLever):
        timesOptimalLeverIsChosen += 1

    updateEstimate(lever, reward)
    updateAverageRewards(reward)
    walkLevers()

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

print()

print("% Optimal lever was chosen")
print(str((timesOptimalLeverIsChosen / NUMBER_OF_ITERATIONS) * 100) + "%")

print()

plt.plot(averageRewards)
plt.ylabel("Average rewards")
plt.xlabel("Step")
plt.show()
