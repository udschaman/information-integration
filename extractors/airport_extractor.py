import csv
import utils.db_utils as util
import os
import datetime
from extractors import extractdb
from timeit import default_timer as timer


createAirportsTable = "CREATE TABLE IF NOT EXISTS airports(airport_id TEXT, name TEXT, city TEXT, country TEXT, iatafaa VARCHAR(3), icao VARCHAR(4), latitude DOUBLE PRECISION, longitude DOUBLE PRECISION, altitude INTEGER, timezone DOUBLE PRECISION, dst VARCHAR(1), tz TEXT);"

util.executeSingleInsertOrCreate(createAirportsTable, extractdb)
util.executeSingleInsertOrCreate("DELETE FROM airports", extractdb)

try:

    insertAirports = "INSERT INTO airports(airport_id, name, city, country, iatafaa, icao, latitude, longitude, altitude, timezone, dst, tz) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"

    dir = os.path.dirname(__file__)
    filename = os.path.join(dir, '../sources/airports.dat')
    dataSet = open(filename, 'r')
    reader = csv.reader(dataSet)
    rowsList = []
    start = timer()
    for row in reader:
        tuple = ()
        for col in row:
            tuple += (col,)
        rowsList.append(tuple)

    util.bulkInsert(insertAirports, rowsList, extractdb)
    end = timer()
    totalTime = end - start
finally:
    dataSet.close()
    print("Airports data was successfully extracted")
    print("Total execution time: " + str(datetime.timedelta(seconds=int(totalTime))))