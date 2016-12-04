import utils.db_utils as util
import utils.general_utils as general
from integration import integratedb
from extractors import extractdb
from dateutil import parser

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

for event in sightingsList:
    t = ()
    try:
        dt = parser.parse(event[0])
    except:
        malformedDateTuples.append(event)
        continue
    t += (dt, )
    key = general.buildLocStateString(event[1], event[2])
    try:
        t += (citiesDict[key],)
    except:
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

print("Malformed dates count: " + str(len(malformedDateTuples)))
print("Malformed cities count: " + str(len(malformedCityTuples)))
print("Malformed shapes count: " + str(len(malformedShapeTuples)))

#TODO: process malformed tuples