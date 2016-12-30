import utils.db_utils as util
import utils.general_utils as general
from integration import integratedb
from extractors import extractdb
from dateutil import parser

import collections
import Levenshtein
import re
import datetime

util.executeSingleInsertOrCreate("CREATE TABLE IF NOT EXISTS ufosightings(event_id SERIAL PRIMARY KEY, tdate TIMESTAMP, city_id INT REFERENCES cities (city_id), shape_id INT REFERENCES shapes (shape_id), duration TEXT, summary TEXT, url TEXT);", integratedb)

util.executeSingleInsertOrCreate("SELECT setval('ufosightings_event_id_seq', 1)", integratedb)
util.executeSingleInsertOrCreate("DELETE FROM ufosightings", integratedb)

shapesList = util.executeSelect("SELECT shape_id, shape_name from shapes", integratedb)
shapesDict = {}

for shape in shapesList:
    shapesDict[shape[1]] = shape[0]

citiesList = util.executeSelect("SELECT DISTINCT city_id, city_name, lower(state_code) FROM cities c JOIN states s ON c.state_id=s.state_id", integratedb)
citiesDict = {}

for city in citiesList:
    key = general.buildLocStateString(city[1], city[2])
    citiesDict[key] = city[0]

sightingsList = util.executeSelect("SELECT date_time, lower(city), lower(state), lower(shape), duration, summary, href FROM ufosightings WHERE state IN (SELECT code FROM states)", extractdb)

insertSightings = "INSERT INTO ufosightings (tdate, city_id, shape_id, duration, summary, url) VALUES (%s, %s, %s, %s, %s, %s)"

normEventsList = []
malformedDateTuples = []
malformedCityTuples = []
malformedShapeTuples = []

city_name_treshold = 0.75

for event in sightingsList:
    t = ()

    try:
        dt = parser.parse(event[0])
    except:
        malformedDateTuples.append(event)
        continue

    t += (dt, )
    key = general.buildLocStateString(event[1], event[2])

    # remove parentheses and last whitespace (to get rid of additional annotations
    key = re.sub(r'[\({\[<].+?[\)}\]>]', '', key).rstrip()
    #remove stuff afer a "/" and ","
    key = key.split('/', 1)[0]
    key = key.split(',', 1)[0]

    #as the cities database has non of these shortcuts, set them to the whole word
    if("st." in key):
        key = key.replace("st.", "saint", 1)

    if("mt." in key):
        key = key.replace("mt.", "mount", 1)

    if("ft." in key):
        key = key.replace("ft.", "fort", 1)

    if(key in citiesDict):
        t += (citiesDict[key],)
    else:
        #some cities like New York are sometimes named New York and sometime New York City. As the cities-db uses the name without the "City" part, we remove it
        if(key.endswith("city")):
            key = key.replace("city", "", 1)
        if(key in citiesDict):
            t += (citiesDict[key],)
        else:
            #the following city name doesn't fit with the names of the city-db
            #to get the cases with wrong written city names, we calculate the levenshtein ratio between the city name and the names of the city-db
            #if the ratio is creater than our treshold, we assume, that the names are just written wrong and use the name of the city-db
            currentMax = 0
            currentTemp = 0
            currentKey = ""
            for element in citiesDict:
                if(element.startswith(key[:3])):
                    currentTemp = Levenshtein.ratio(key[3:], element)
                    if(currentTemp > currentMax):
                        currentMax = currentTemp
                        currentKey = element

            if(currentMax >= city_name_treshold):
                t += (citiesDict[currentKey],)
            else:
                malformedCityTuples.append(event)
                continue

    try:
        t += (shapesDict[event[3]],)
    except:
        malformedShapeTuples.append(event)
        continue

    t += (event[4],)
    t += (event[5],)
    t += (event[6],)

    normEventsList.append(t)

util.bulkInsert(insertSightings, normEventsList, integratedb)

## as the dates are just 118 cases and they are a mess, i would say, we drop them
print("Malformed dates count: " + str(len(malformedDateTuples)))
print("Malformed cities count: " + str(len(malformedCityTuples)))
print("Malformed shapes count: " + str(len(malformedShapeTuples)))
