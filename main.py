from typing import Final
from DoRun import run
import matplotlib.pyplot as plt

NUMBER_OF_RUNS: Final = 20
allAverageRewardsIncremental: list[list[float]] = []
allAverageRewardsWeighted: list[list[float]] = []

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
    print(str(round(((i + 1) / NUMBER_OF_RUNS) * 100, 2)) + "%")

for i in range(NUMBER_OF_RUNS):
    singleRun = run(useIncrementalEstimateCalculation=False)
    allAverageRewardsWeighted.append(singleRun['averageRewards'])
    print(str(round(((i + 1) / NUMBER_OF_RUNS) * 100, 2)) + "%")

plt.plot(getSingleListOfAverages(allAverageRewardsIncremental), 'r')
plt.plot(getSingleListOfAverages(allAverageRewardsWeighted), 'b')
plt.ylabel("Average reward over " + str(NUMBER_OF_RUNS) + " runs")
plt.xlabel("Step")
plt.show()
