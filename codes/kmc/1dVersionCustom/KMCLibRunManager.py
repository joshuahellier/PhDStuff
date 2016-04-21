import subprocess

# This code is meant to manage running multiple instances of my KMCLib codes at the same time,
# in the name of time efficiency

numCores = 6
totalRuns = 12
avConc = 0.5
maxConcDiff = 1.0
minConcDiff = -1.0
numSteps = 200000000
transTime = 5000000.0
fullRate = 1.0
sysSize = 8
dataLocation = "tests/pythonManagerTest11/"

concStepSize = (maxConcDiff-minConcDiff)/float(totalRuns-1)
jobsStarted = 0
coresUsed = 0

runningJobs = []

while jobsStarted<totalRuns:
    coresUsed = 0
    runningJobs = []
    while (coresUsed<numCores) and (jobsStarted<totalRuns):
#        jobInput = ["python 1dCustom.py", str(avConc), str(minConcDiff+float(jobsStarted)*concStepSize), str(fullRate), str(sysSize), str(numSteps), str(transTime), dataLocation+str(jobsStarted)]
        jobInput = "python 1dCustom.py "+str(avConc)+" "+str(minConcDiff+float(jobsStarted)*concStepSize)+" "+str(fullRate)+" "+str(sysSize)+" "+str(numSteps)+" "+str(transTime)+" "+dataLocation+str(jobsStarted)+" >/dev/null"
        p = subprocess.Popen(jobInput, shell=True)
        runningJobs.append(p)
        print "Starting job "+str(jobsStarted+1)+" on core "+str(coresUsed+1)
        coresUsed += 1
        jobsStarted += 1
    exit_codes = [p.wait() for p in runningJobs]
print "All runs complete."
