import subprocess
import sys
import os
import math

# This code is meant to manage running multiple instances of my KMCLib codes at the same time,
# in the name of time efficiency
numLambda = 128
numDensDiff = 128
sysSize = 10
numTimeSlices = 20
numVecs = 2
dataLocation = "exactSolns/densityLambdaRuns/secondAttempt/"
lambdaMin = 10.0**(-3)
lambdaMax = 10.0**(2)
densMin = 0.001
densMax = 0.999
densDiff = 0.001
botDensMax = densMax
botDensMin = densMin+densDiff
rateStepSize = (lambdaMax-lambdaMin)/float(numLambda-1)
densStepSize = (botDensMax-botDensMin)/float(numDensDiff-1)
jobIndex = 1
boundMult = 100.0
tolerance = 10.0**(-18)
runningJobs = []

for rateIndex in range(0, numLambda):
    tempRate = lambdaMin + rateStepSize*rateIndex
#    currentRate = tempRate
    currentRate = math.exp(((tempRate-lambdaMin)*math.log(lambdaMax)+(lambdaMax-tempRate)*math.log(lambdaMin))/(lambdaMax-lambdaMin))
    for densIndex in range(0, numDensDiff):
        botConc = densStepSize*densIndex+botDensMin
        topConc = botConc - densDiff
        jobInput = "simpleGroundStateFinder.py "+str(botConc)+" "+str(topConc)+" "+str(currentRate)+" "+str(sysSize)+" "+str(numVecs)+" "+str(boundMult)+" "+str(tolerance)+" "+str(numTimeSlices)+" "+dataLocation+str(rateIndex)+"/"+str(densIndex)+"\n"
        with open("jobInputs/testInput."+str(jobIndex), 'w') as f:
            f.write(jobInput)
            jobIndex += 1
