from DoRun import run
import timeit

timeTakenWeighted = timeit.timeit("run(useIncrementalEstimateCalculation=False)", globals=globals(), number=10)
timeTakenIncremental = timeit.timeit("run(useIncrementalEstimateCalculation=True)", globals=globals(), number=10)

print("Time taken weighted is " + str(timeTakenWeighted))
print("Time taken incremental is " + str(timeTakenIncremental))
