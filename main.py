from typing import Final
from DoRun import run
import matplotlib.pyplot as plt

NUMBER_OF_RUNS: Final = 2000
allAverageRewardsIncremental: list[list[float]] = []
allAverageRewardsWeighted: list[list[float]] = []

allPercentageOfOptimalLeverChosenIncremental: list[list[float]] = []
allPercentageOfOptimalLeverChosenWeighted: list[list[float]] = []

def getSingleListOfAverages(listContainingListsOfAverages: list[list[float]]):
    singleListOfAverages: list[float] = []
    for i in range(len(listContainingListsOfAverages[0])):
        average = 0
        for _,listOfAverages in enumerate(listContainingListsOfAverages):
            average += listOfAverages[i]
        average /= len(listContainingListsOfAverages)
        singleListOfAverages.append(average)
    return singleListOfAverages

for i in range(NUMBER_OF_RUNS):
    singleRun = run(useIncrementalEstimateCalculation=True)
    allAverageRewardsIncremental.append(singleRun['averageRewards'])
    allPercentageOfOptimalLeverChosenIncremental.append(singleRun['percentageOfOptimalLeverChosen'])
    print(str(round(((i + 1) / (NUMBER_OF_RUNS * 2)) * 100, 2)) + "%")

for i in range(NUMBER_OF_RUNS):
    singleRun = run(useIncrementalEstimateCalculation=False)
    allAverageRewardsWeighted.append(singleRun['averageRewards'])
    allPercentageOfOptimalLeverChosenWeighted.append(singleRun['percentageOfOptimalLeverChosen'])
    print(str(round(((i + 1 + NUMBER_OF_RUNS) / (NUMBER_OF_RUNS * 2)) * 100, 2)) + "%")

plt.subplot(121)
plt.plot(getSingleListOfAverages(allAverageRewardsIncremental), 'r')
plt.plot(getSingleListOfAverages(allAverageRewardsWeighted), 'b')
plt.ylabel("Average reward over " + str(NUMBER_OF_RUNS) + " runs")
plt.xlabel("Step")

plt.subplot(122)
plt.plot(getSingleListOfAverages(allPercentageOfOptimalLeverChosenIncremental), 'r')
plt.plot(getSingleListOfAverages(allPercentageOfOptimalLeverChosenWeighted), 'b')
plt.ylabel("Average percentage of optimal lever chosen over " + str(NUMBER_OF_RUNS) + " runs")
plt.xlabel("Step")

plt.show()
