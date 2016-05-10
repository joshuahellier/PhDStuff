import sys
import os
import numpy
import cPickle as pickle
import postProcessorUtilities

resultDir = os.environ.get('RESULTS')
if resultDir == None :
    print "WARNING! $RESULTS not set! Attempt to write results will fail!\n"

fileInfo = sys.argv[1]
resultsPlace = resultDir+"/"+fileInfo+"/"

if not os.path.exists(resultsPlace):
    print"WARNING! The results directory requested does not exist! Perhaps there is some typo...\n"
    exit()

directoryList = os.listdir(resultsPlace)

resultsTable = []
lines = []
words = []

g = open(resultsPlace+"regressionData.dat", 'w')

for i in directoryList:
    sites = []
    times = []
    steps = []
    types = []
    typesTimeAverage = []
    currentDir = resultsPlace+i

    execfile(currentDir+"/traj.tr")

    with open(currentDir + "/settings", 'r') as f:
        lines = f.readlines()
    words = (lines[1]).split()
    diffConc = float(words[2])
    words = (lines[3]).split()
    sysSize = int(words[2])
    words = (lines[3]).split()
    timeInterval = int(words[2])

    with open(currentDir + "/procOxInTop.dat", 'r') as f:
        lines = f.readlines()
    words = (lines[-1]).split()
    rateAndErr = (words[12]).split('+/-')
    topInRate = rateAndErr[0]
    topInErr = rateAndErr[1]

    with open(currentDir + "/procOxOutTop.dat", 'r') as f:
        lines = f.readlines()
    words = (lines[-1]).split()
    rateAndErr = (words[12]).split('+/-')
    topOutRate = rateAndErr[0]
    topOutErr = rateAndErr[1]

    with open(currentDir + "/procOxInBot.dat", 'r') as f:
        lines = f.readlines()
    words = (lines[-1]).split()
    rateAndErr = (words[12]).split('+/-')
    botInRate = rateAndErr[0]
    botInErr = rateAndErr[1]

    with open(currentDir + "/procOxOutBot.dat", 'r') as f:
        lines = f.readlines()
    words = (lines[-1]).split()
    rateAndErr = (words[12]).split('+/-')
    botOutRate = rateAndErr[0]
    botOutErr = rateAndErr[1]

    resultsTable.append([diffConc, (float(topInRate), float(topInErr)), (float(topOutRate), float(topOutErr)), (float(botInRate), float(botInErr)), (float(botOutRate), float(botOutErr))])

    print("Testing!\n")
    # Now to try to work out time-averaged occupation from the traj.tr files.
    weightings = []
    chunklets = []
    currentChunklet = []
    timeChunkIndex = 0
    mainIndex = 0
    """Just for now!"""
    timeInterval = 100000.0
    for j in times:
        print(j)
        if float(j) < float(timeChunkIndex+1)*timeInterval:
            currentChunklet.append(mainIndex)
        else:
            chunklets.append(currentChunklet)
            currentChunklet = []
            currentChunklet.append(mainIndex)
            timeChunkIndex = timeChunkIndex+1
        mainIndex = mainIndex + 1

    timeChunkIndex = 0
    mainIndex = 0
    listIndex = 0
    weights = []
    for j in chunklets:
        currentWeights = []
        chunkIndex = 0
        currentWeight = 0.0
        currentWeight = 0.5*((times[j[0]]-timeChunkIndex*timeInterval)**2)/(times[j[0]]-times[mainIndex-1])
        currentWeights.append([j[0]-1, currentWeight])
        for k in j:
            currentWeight = 0.0
            if chunkIndex == 0:
                currentWeight += 0.5*(times[k]-timeChunkIndex*timeInterval)
            else:
                currentWeight += 0.5*(times[k]-times[k-1])
            if chunkIndex == len(j)-1:
                currentWeight += 0.5*((timeChunkIndex+1)*timeInterval-times[k])
            else:
                currentWeight += 0.5*(times[k+1]-times[k])
            currentWeights.append([k, currentWeight])
            mainIndex = mainIndex + 1
            chunkIndex = chunkIndex + 1
        currentWeight = 0.5*(((timeChunkIndex+1)*timeInterval-times[j[-1]])**2)/(times[mainIndex+1]-times[j[-1]])
        currentWeights.append([j[-1]+1, currentWeight])
        timeChunkIndex = timeChunkIndex + 1
    weights.append(currentWeights)
    
    print("Now let's see what these weights are!\n")

    for j in weights:
        for k in j:
            print(str(k)+"\n")

    print("Done testing!\n")
            
    #print(str(diffConc)+" "+topInRate+" "+topInErr+" "+topOutRate+" "+topOutErr+" "+botInRate+" "+botInErr+" "+botOutRate+" "+botOutErr)
    g.write(str(diffConc)+" "+topInRate+" "+topInErr+" "+topOutRate+" "+topOutErr+" "+botInRate+" "+botInErr+" "+botOutRate+" "+botOutErr+"\n")
g.write("\n")
g.close()
pickle.dump(resultsTable, open(resultsPlace+"mainResults.p", "wb"))

flow = []
flowErr = []
gradient = []

for i in resultsTable:
    flow.append(i[1][0]+i[4][0]-i[2][0]-i[3][0])
    flowErr.append(numpy.sqrt(i[1][1]**2+i[4][1]**2+i[2][1]**2+i[3][1]**2))
    gradient.append(i[0]/float(sysSize))
    print(str(gradient[-1])+" "+str(flow[-1])+" "+str(flowErr[-1]))

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.formula.api as sm

x_list = gradient
y_list = flow
y_err = flowErr

# put x and y into a pandas DataFrame, and the weights into a Series
ws = pd.DataFrame({
    'x': x_list,
    'y': y_list
})
weights = pd.Series(y_err)

wls_fit = sm.wls('x ~ y', data=ws, weights=1.0 / ((weights)**2)).fit()
ols_fit = sm.ols('x ~ y', data=ws).fit()

# show the fit summary by calling wls_fit.summary()
# wls fit r-squared is 0.754
# ols fit r-squared is 0.701

with open(resultsPlace+"regressionData.dat", 'a') as f:
    f.writelines([str(wls_fit.summary())+"\n", str(wls_fit.params[0])+" "+str(wls_fit.bse[0])+"\n", str(wls_fit.params[1])+" "+str(wls_fit.bse[1])+"\n"])
    

