import sys
import os
import numpy
import cPickle as pickle
import postProcessorUtilities as pPU

timeChunkSize = float(sys.argv[2])

resultDir = os.environ.get('RESULTS')
if resultDir == None :
    print "WARNING! $RESULTS not set! Attempt to write results will fail!\n"

fileInfo = sys.argv[1]
resultsPlace = resultDir+"/"+fileInfo+"/"

if not os.path.exists(resultsPlace):
    print"WARNING! The results directory requested does not exist! Perhaps there is some typo...\n"
    exit()



resultsTable = []
lines = []
words = []



#Firstly, get rid of any files which could cause trouble and crash things
fileName = resultsPlace+"mainResults.p"
try:
    os.remove(fileName)
except OSError:
    pass

fileName = resultsPlace+"regressionData.dat"
try:
    os.remove(fileName)
except OSError:
    pass

directoryList = os.listdir(resultsPlace)

g = open(resultsPlace+"regressionData.dat", 'w')

for i in directoryList:

    sites = []
    times = []
    steps = []
    types = []
    typesTimeAverage = []
    currentDir = resultsPlace+i
    print("Considering file "+currentDir+"\n")

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

    weightings = pPU.weightingsFinder(times, timeChunkSize)
    numTypes = len(types[1])
    typeStats = []
    
    with open(currentDir+"/types.dat", "w") as kindFile:
        for typeList in types:
            #print(typeList)
            for kind in range(0, len(typeList)):
                #print(str(kind))
                kindFile.write(typeList[kind])
            kindFile.write("\n")
    
    for typeIndex in range(0, numTypes):
        typeHistory = []
        for chunkWeights in weightings:
            tempTotal = 0.0
            for weight in chunkWeights[1]:
                temp = types[weight[0]]
                if temp[typeIndex] == "O":
                    tempTotal += weight[1]
            typeHistory.append([chunkWeights[0], tempTotal/timeChunkSize])
        typeStats.append(typeHistory)
    
    with open(currentDir+"/typeStats.dat", "w") as typeFile:
        for typeHistory in typeStats:
            for chunk in typeHistory:
                typeFile.write(str(chunk[1])+" ")
            typeFile.write("\n")
            
    

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
    #print(str(gradient[-1])+" "+str(flow[-1])+" "+str(flowErr[-1]))

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
    

