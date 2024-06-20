from collections.abc import Callable
from typing import Final, TypedDict
import time
import random

class Run(TypedDict):
    percentageOfOptimalLeverChosen: list[float]
    averageRewards: list[float]

updatePercentageOfOptimalLeverChosenTime = 0
updateEstimateTime = 0
updateAverageRewardsTime = 0
walkLeversTime = 0

def run(useIncrementalEstimateCalculation: bool) -> Run:
    CHANCE_TO_SELECT_RANDOMLY: Final = 0.1
    STEP_SIZE_PARAMETER: Final = 0.1

    NUMBER_OF_ITERATIONS: Final = 10000

    ARE_LEVERS_WALKING: Final = True

    DEFAULT_ESTIMATE: Final = 0

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
        trueValue = random.normalvariate(0, 1)
        def takeRandomWalk():
            nonlocal trueValue
            trueValue += random.normalvariate(0, 0.01)
        return {
            "estimate": None,
            "getReward": lambda: random.normalvariate(trueValue, 1),
            "takeRandomWalk": takeRandomWalk,
            "getTrueValue": lambda: trueValue
        }

    def getOptimalLever(levers: list[Lever]):
        optimalLever = levers[0]
        for lever in levers:
            if (optimalLever["getTrueValue"]() < lever["getTrueValue"]()):
                optimalLever = lever
        return optimalLever

    def chooseLeverRandomly():
        return random.choice(levers)

    def chooseLeverGreedily():
        def getHighestEstimateLevers(list: list[Lever]) -> list[Lever]:
            highestEstimate = -999
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

    averageRewards: list[float] = []

    optimalLever = getOptimalLever(levers)
    percentageOfOptimalLeverChosen: list[float] = []

    for i in range(NUMBER_OF_ITERATIONS):
        def chooseLever():
            if (random.random() < CHANCE_TO_SELECT_RANDOMLY):
                return chooseLeverRandomly()
            else:
                return chooseLeverGreedily()

        def updateEstimate(lever, reward):
            if (lever['estimate'] is None):
                lever['estimate'] = reward
            else:
                if (useIncrementalEstimateCalculation):
                    lever['estimate'] = calculateNewAverageIncrementally(lever['estimate'], reward, i + 1)
                else:
                    lever['estimate'] = calculateNewAverageWithStepSizeParameter(lever['estimate'], reward, STEP_SIZE_PARAMETER)

        def updateAverageRewards(reward):
            nonlocal averageRewards
            if (i == 0):
                averageRewards.append(reward)
            else:
                averageRewards.append(
                    calculateNewAverageIncrementally(averageRewards[i - 1], reward, i + 1)
                )

        def updatePercentageOfOptimalLeverChosen():
            nonlocal percentageOfOptimalLeverChosen
            leverChosenWasOptimalAsInt = 1 if lever is optimalLever else 0
            if (i == 0):
                percentageOfOptimalLeverChosen.append(leverChosenWasOptimalAsInt)
            else:
                percentageOfOptimalLeverChosen.append(
                    calculateNewAverageIncrementally(percentageOfOptimalLeverChosen[i - 1], leverChosenWasOptimalAsInt, i + 1)
                )

        def walkLevers():
            if (ARE_LEVERS_WALKING):
                for _,lever in enumerate(levers):
                    lever["takeRandomWalk"]()

        lever = chooseLever()
        reward = lever['getReward']()

        global updatePercentageOfOptimalLeverChosenTime, updateEstimateTime, updateAverageRewardsTime, walkLeversTime

        start_time = time.time()
        updatePercentageOfOptimalLeverChosen()
        end_time = time.time()
        elapsed = end_time - start_time
        updatePercentageOfOptimalLeverChosenTime += elapsed

        start_time = time.time()
        updateEstimate(lever, reward)
        end_time = time.time()
        elapsed = end_time - start_time
        updateEstimateTime += elapsed

        start_time = time.time()
        updateAverageRewards(reward)
        end_time = time.time()
        elapsed = end_time - start_time
        updateAverageRewardsTime += elapsed

        start_time = time.time()
        walkLevers()
        end_time = time.time()
        elapsed = end_time - start_time
        walkLeversTime += elapsed
    

    print("updatePercentageOfOptimalLeverChosenTime = " + str(updatePercentageOfOptimalLeverChosenTime))
    print("updateEstimateTime = " + str(updateEstimateTime))
    print("updateAverageRewardsTime = " + str(updateAverageRewardsTime))
    print("walkLeversTime = " + str(walkLeversTime))

    return {
        "percentageOfOptimalLeverChosen": percentageOfOptimalLeverChosen,
        "averageRewards": averageRewards
    }
