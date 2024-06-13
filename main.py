import matplotlib.pyplot as plt
import numpy as np
import random

# Page 31 Second Edition Barto and Sutton
def calculateNewAverageIncrementally(oldAverage, nextValue, numberOfValues):
    return oldAverage + (1/numberOfValues) * (nextValue - oldAverage)

averageRewards = []

def firstLever():
    return 1.0

def secondLever():
    return 0.0

def randomLever():
    return firstLever() if random.random() >= 0.5 else secondLever()

for i in range(20):
    if (i == 0):
        averageRewards.append(randomLever())
    else:
        averageRewards.append(
            calculateNewAverageIncrementally(averageRewards[i - 1], randomLever(), i + 1)
        )

print(averageRewards)
