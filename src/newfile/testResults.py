from . import multiCoreTest as test
import matplotlib
import matplotlib.pyplot as plt
import sys

#Args for program

cores = int(sys.argv[3]) #Number of cores to utilize with multiprocessor
runs = int(sys.argv[2]) #Number of times program is to run, with linearly increasing processes
time = float(sys.argv[5]) #Sleep timer to allow child process to join parent
multiplier = int(sys.argv[4]) # Number of processes to increase by in each iteration of for loop

# Arrays used for storing results
timesArray = []
ratioArray =[]

xLabel = 'Processes running *('+ str(multiplier) + ")"
# Run test n times, increasing number of processes to run each time by [multiplier], split between [cores] cores
# append results to arrays
for x in range(1,runs):
        multi, single = test.run(cores,x*multiplier,time)
        timesArray.append((multi,single))
        ratioArray.append((((multi/single)*100)-100)*-1)

# Plot the results: First subplot shows comparison in run time, second subplot shows the reduction (Or increase) in time to run-
# - on multiple cores
plt.subplot(2,1,1)
plt.title(  str(cores) + " cores (blue) vs Single core (Orange)")
plt.ylabel('Time to run (s)')
plt.plot(timesArray)

plt.subplot(2,1,2)
plt.xlabel(xLabel)
plt.ylabel("Reduction in time (%)")
plt.plot(ratioArray)
plt.show()
