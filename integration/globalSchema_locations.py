
import utils.db_utils as util
import utils.general_utils as general
from integration import integratedb
from extractors import extractdb
from collections import defaultdict, Counter
from timeit import default_timer as timer
import datetime
threshold = 0.35

start = timer()

createCitiesTable = "CREATE TABLE IF NOT EXISTS cities(city_id SERIAL PRIMARY KEY, city_name TEXT, state_id INT REFERENCES states (state_id), lat REAL, lon REAL);"

util.executeSingleInsertOrCreate(createCitiesTable, integratedb)
util.executeSingleInsertOrCreate("SELECT setval('cities_city_id_seq', 1)", integratedb)
util.executeSingleInsertOrCreate("DELETE FROM cities", integratedb)

statesList = util.executeSelect("SELECT state_id, lower(state_code) from states", integratedb)
statesDict = {}

for state in statesList:
    statesDict[state[1]] = state[0]

selectAvgLocationInfo = "SELECT lower(city), lower(state), AVG(lat)::numeric(16,2) as latitude, AVG(lon)::numeric(16,2) as longtitude FROM locations WHERE lower(state) IN (SELECT lower(code) FROM states) AND lat IS NOT NULL AND lon IS NOT NULL AND location_type='PRIMARY' GROUP BY city, state HAVING MAX(lat)-MIN(lat)<=" + str(threshold) + "  AND MAX(lon)-MIN(lon)<=" + str(threshold) + " ORDER BY state"

normLocationsInfo = util.executeSelect(selectAvgLocationInfo, extractdb)

insertLocations = "INSERT INTO cities (city_name, state_id, lat, lon) VALUES (%s, %s, %s, %s)"
locInsert = []
for location in normLocationsInfo:
    locInsert.append((location[0], statesDict[location[1]], location[2], location[3],))

util.bulkInsert(insertLocations, locInsert, integratedb)

selectProblematicLocations = "SELECT lower(t.city), lower(t.state), l.lat, l.lon FROM locations l JOIN (SELECT city, lower(state) AS state FROM locations WHERE lower(state) IN (select lower(code) FROM states) AND lat IS NOT NULL AND lon IS NOT NULL AND location_type='PRIMARY' GROUP BY city, state HAVING MAX(lat)-MIN(lat)>" + str(threshold) + " OR MAX(lon)-MIN(lon)>" + str(threshold) + " order by city, state ) t ON t.city = l.city AND t.state=lower(l.state)"

dirtyLocationsInfo = util.executeSelect(selectProblematicLocations, extractdb)
dirtyStateLocDict = defaultdict(list)
for loc in dirtyLocationsInfo:
    key = general.buildLocStateString(loc[0], loc[1])
    if not dirtyStateLocDict[key]:
        dirtyStateLocDict[key] = [loc[0], loc[1], [], []]

    dirtyStateLocDict[key][2].append(loc[2])
    dirtyStateLocDict[key][3].append(loc[3])

cleanedLocations = []
for key in dirtyStateLocDict.keys():
    stateId = statesDict[dirtyStateLocDict[key][1]]
    tuple = (dirtyStateLocDict[key][0], stateId,)

    latList = dirtyStateLocDict[key][2]

    lat = None
    if max(latList)-min(latList) > threshold:
        b = Counter(latList)
        if (b.most_common(1)[0][1] > 1):
           lat = b.most_common(1)[0][0]
        else:
            if len(latList)>2:
                lat = general.getBestEffortValue(latList, threshold)
            else:
                lat = round(sum(latList) / float(len(latList)), 3)
    else:
        lat = round(sum(latList)/float(len(latList)), 3)


    lonList = dirtyStateLocDict[key][3]
    lon = None
    if max(lonList) - min(lonList) > threshold:
        b = Counter(lonList)
        if (b.most_common(1)[0][1] > 1):
            lon = b.most_common(1)[0][0]
        else:
            if len(lonList)>2:
                lon = general.getBestEffortValue(lonList, threshold)
            else:
                lon = round(sum(lonList) / float(len(lonList)), 3)
    else:
        lon = round(sum(lonList) / float(len(lonList)), 3)

    tuple += (lat,)
    tuple += (lon,)
    cleanedLocations.append(tuple)

util.bulkInsert(insertLocations, cleanedLocations, integratedb)

end = timer()
totalTime = end - start

print("locations data was successfully cleaned and inserted into the global schema")
print("Total execution time: " + str(datetime.timedelta(seconds=int(totalTime))))