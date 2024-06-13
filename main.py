import matplotlib.pyplot as plt
import numpy as np

# Page 31 Second Edition Barto and Sutton
def calculateNewAverageIncrementally(oldAverage, nextValue, numberOfValues):
    return oldAverage + (1/numberOfValues) * (nextValue - oldAverage)
