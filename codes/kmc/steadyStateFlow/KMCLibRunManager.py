import subprocess
import sys
import os

# This code is meant to manage running multiple instances of my KMCLib codes at the same time,
# in the name of time efficiency

numCores = 6
totalRuns = 12
botConc = 1.0
topConc = 0.0
numSteps = 10000000
transTime = 1000.0
sysSize = 128
analInterval = 10
timeInterval = 5000.0
dataLocation = "steadyStateFlow/tests/exploratory/1/"
fullRateMin = 0.01
fullRateMax = 2.0
rateStepSize = (fullRateMax-fullRateMin)/float(totalRuns-1)

jobsStarted = 0
coresUsed = 0

runningJobs = []

while jobsStarted<totalRuns:
    coresUsed = 0
    runningJobs = []
    while (coresUsed<numCores) and (jobsStarted<totalRuns):
#        jobInput = ["python 1dCustom.py", str(avConc), str(minConcDiff+float(jobsStarted)*concStepSize), str(fullRate), str(sysSize), str(numSteps), str(transTime), dataLocation+str(jobsStarted)]
        jobInput = "python steadyStateFlow.py "+str(botConc)+" "+str(topConc)+" "+str(jobsStarted*rateStepSize+fullRateMin)+" "+str(sysSize)+" "+str(analInterval)+" "+str(numSteps)+" "+str(timeInterval)+" "+str(transTime)+" "+dataLocation+str(jobsStarted)+" >/dev/null"
        p = subprocess.Popen(jobInput, shell=True)
        runningJobs.append(p)
        print "Starting job "+str(jobsStarted+1)+" on core "+str(coresUsed+1)
        coresUsed += 1
        jobsStarted += 1
    exit_codes = [p.wait() for p in runningJobs]
print "All runs complete."
