def buildLocStateString(city, state):
    return (str(state).strip() + "_" + str(city).replace(" ", "")).lower()

def getBestEffortValue(array, threshold):
    if(len(array) < 3):
        return round(sum(array) / float(len(array)), 3)

    if max(array)-min(array) > threshold:
        extremaToRemove = chooseExtremaToRemove(list(array))
        array.remove(extremaToRemove)
        getBestEffortValue(array, threshold)

    return round(sum(array)/float(len(array)), 3)

def chooseExtremaToRemove(array):
    maxValue = max(array)
    minValue = min(array)
    array.remove(maxValue)
    array.remove(minValue)
    avg = round(sum(array)/float(len(array)), 3)
    dif_max = maxValue-avg
    dif_min = minValue-avg
    if (dif_max > dif_min):
        return maxValue
    else:
        return minValue