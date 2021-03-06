def weightingsFinder(times, timeInterval):
    """This finds a load of weightings, so that one can integrate linearly-interpolated data"""
    
    #This first bit works out which times fall into which time interval
    
    timeChunkIndex = 0
    chunklets = []
    mainIndex = 0
    currentChunklet = []
    while mainIndex < len(times):
        if float(times[mainIndex]) < float(timeChunkIndex+1)*timeInterval+times[0]:
            currentChunklet.append(mainIndex)
            mainIndex += 1
            if mainIndex == len(times):
                chunklets.append(currentChunklet)
        else:
            chunklets.append(currentChunklet)
            currentChunklet = []
            timeChunkIndex = timeChunkIndex+1
    
    #This next bit takes the time chunks and works out the weightings of the relevant time indices for specific time chunks
    
    mainIndex = 0
    timeChunkIndex = 0
    weight = 0.0
    weightings = []
    temporaryWeightings = []
    for j in chunklets:
        temporaryWeightings = []
    
    
        if len(j) == 0:
            #In this case, we work out the contributions from the current and next mainIndexed points
            weight = 0.5*timeInterval
            temporaryWeightings.append([mainIndex, weight])
            temporaryWeightings.append([mainIndex+1, weight]) 
    
    
        if len(j) == 1:
            mainIndex = j[0]
            #Now there's three contributions, usually
            if mainIndex != 0 and mainIndex < len(times)-1:
                a = times[mainIndex-1]
                b = timeChunkIndex*timeInterval+times[0]
                c = times[mainIndex]
                d = (timeChunkIndex+1)*timeInterval+times[0]
                e = times[mainIndex+1]
    
                weight = 0.5*((c-b)**2)/(c-a)
                temporaryWeightings.append([mainIndex-1, weight])
    
                weight = 0.5*((c-b)*(b+c-2.0*a)/(c-a)+(d-c)*(2.0*e-c-d)/(e-c))
                temporaryWeightings.append([mainIndex, weight])
    
                weight = 0.5*((d-c)**2)/(e-c)
                temporaryWeightings.append([mainIndex+1, weight])
            else:
                if mainIndex == 0:
                    # If the point happens to be the first, there's only 2 weightings to consider
                    b = times[0]
                    c = timeInterval
                    d = times[1]
                    weight = 0.5*((d-b)**2-(d-c)**2)/(d-b)
                    temporaryWeightings.append([0, weight])
                    weight = 0.5*(c-b)**2/(d-b)
                    temporaryWeightings.append([1, weight])
                else:
                    #If the point happens to be the last, same idea
                    d = (timeChunkIndex+1)*timeInterval + times[0]
                    c = times[-1]
                    b = timeChunkIndex*timeInterval + times[0]
                    a = times[-2]
                    weight = 0.5*(c-b)**2/(c-a)
                    temporaryWeightings.append([mainIndex-1, weight])
                    weight = (d-c) + 0.5*((c-a)**2-(b-a)**2)/(c-a)
                    temporaryWeightings.append([mainIndex, weight])
        
    
        if len(j) > 1:
            #otherwise
            mainIndex = j[0]
            #First bit concerns the previous timePoint (if it exists!)
            weight = 0.0
            if mainIndex != 0:
                a = times[mainIndex-1]
                b = timeChunkIndex*timeInterval+times[0]
                c = times[mainIndex]
                d = times[mainIndex+1]
                weight = 0.5*(c-b)**2/(c-a)
                temporaryWeightings.append([mainIndex-1, weight])
                weight = 0.5*((c-a)**2-(b-a)**2)/(c-a)+0.5*(d-c)
                temporaryWeightings.append([mainIndex, weight])
            else:
                b = times[0]
                d = times[1]
                weight = 0.5*(d+b)
                temporaryWeightings.append([mainIndex, weight])
    
            #Main body, actually fairly simple for a change! 
            for mainIndex in range(j[1], j[-1]):
                a = times[mainIndex-1]
                c = times[mainIndex+1]
                weight = 0.5*(c-a)
                temporaryWeightings.append([mainIndex, weight])
    
            mainIndex = j[-1]
            if mainIndex == len(times)-1:
                c = timeInterval*(timeChunkIndex+1)+times[0]
                b = times[-1]
                a = times[-2]
                weight = (c-b) + 0.5*(b-a)
                temporaryWeightings.append([mainIndex, weight])
            else:
                d = times[mainIndex+1]
                c = timeInterval*(timeChunkIndex+1)+times[0]
                b = times[mainIndex]
                a = times[mainIndex-1]
                weight = 0.5*(b-a)+0.5*((d-b)**2-(d-c)**2)/(d-b)
                temporaryWeightings.append([mainIndex, weight])
                weight = 0.5*(c-b)**2/(d-b)
                temporaryWeightings.append([mainIndex+1, weight])
       

        weightings.append([timeChunkIndex, temporaryWeightings])
        timeChunkIndex += 1
    return weightings
