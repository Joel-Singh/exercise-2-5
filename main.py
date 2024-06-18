from typing import Final
from DoRun import run

NUMBER_OF_RUNS: Final = 2000
allAverageRewards: list[list[float]] = []
allPercentageOfOptimalLeverChosen: list[list[float]] = []


def getAveragedAveragedRewards():
    averagedAveragedRewards: list[float] = []
    for i in range(len(allAverageRewards[0])):
        average = 0
        for _,averageRewards in enumerate(allAverageRewards):
            average += averageRewards[i]
        average /= len(allAverageRewards)
        averagedAveragedRewards.append(average)
    return averagedAveragedRewards

for i in range(NUMBER_OF_RUNS):
    singleRun = run(True)
    allAverageRewards.append(singleRun['averageRewards'])
    allPercentageOfOptimalLeverChosen.append(singleRun['percentageOfOptimalLeverChosen'])
    print(str(round(((i + 1) / NUMBER_OF_RUNS) * 100, 2)) + "%")

print(getAveragedAveragedRewards())
