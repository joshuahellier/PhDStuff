import sys
import os
import numpy
import subprocess


resultDir = os.environ.get('RESULTS')
if resultDir == None :
    print ("WARNING! $RESULTS not set! Attempt to write results will fail!\n")

fileInfo = sys.argv[1]
resultsPlace = resultDir+"/"+fileInfo+"/"

if not os.path.exists(resultsPlace):
    print ("WARNING! The results directory requested does not exist! Perhaps there is some typo...\n")
    exit()



#Firstly, get rid of any files which could cause trouble and crash things


topDirectoryList = os.listdir(resultsPlace)
fullRate = 0.0
avConc = 0.0

jobIndex = 1

for topLevel in topDirectoryList:
    fileName = resultsPlace+topLevel+"/overallData.dat"
    try:
        os.remove(fileName)
    except OSError:
        pass
    fileName = resultsPlace+topLevel+"/grandConcData.dat"
    try:
        os.remove(fileName)
    except OSError:
        pass
    midDirectoryList = os.listdir(resultsPlace+topLevel)
    for midLevel in midDirectoryList:
        location = fileInfo+"/"+topLevel+"/"+midLevel
        jobInput = "postProcessor.py "+location+"\n"
        with open("postProcInputs/postProcInput."+str(jobIndex), 'w') as f:
            f.write(jobInput)
        jobIndex += 1
