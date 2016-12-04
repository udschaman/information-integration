import csv
import os
import datetime
import utils.db_utils as util
from extractors import extractdb
from timeit import default_timer as timer

createLocationsTable = "CREATE TABLE IF NOT EXISTS locations(rec_num INTEGER, zip INTEGER, zip_type TEXT, city TEXT, state VARCHAR(2), location_type TEXT, lat DOUBLE PRECISION, lon DOUBLE PRECISION, x_axis TEXT, y_axis TEXT, z_axis TEXT, world_region TEXT, country TEXT, loc_text TEXT, location TEXT, decommissioned TEXT, tax_ret TEXT, population TEXT, total_wages TEXT, notes TEXT);"

util.executeSingleInsertOrCreate(createLocationsTable, extractdb)
util.executeSingleInsertOrCreate("DELETE FROM locations", extractdb)

try:
    dir = os.path.dirname(__file__)
    filename = os.path.join(dir, '../sources/free-zipcode-database.csv')
    dataSet = open(filename, 'r')

    reader = csv.reader(dataSet)
    next(reader)

    rowsList = []
    start = timer()
    for row in reader:
        t = ()
        for col in row:
            if not col:
                t += (None,)
            else:
                t += (col,)
        rowsList.append(t)

        insertLocations = "INSERT INTO locations(rec_num, zip, zip_type, city, state, location_type, lat, lon, x_axis, y_axis, z_axis, world_region, country, loc_text, location, decommissioned, tax_ret, population, total_wages, notes) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"

    util.bulkInsert(insertLocations, rowsList, extractdb)
    end = timer()
    totalTime = end - start
finally:
    dataSet.close()
    print("Locations data was successfully extracted")
    print("Total execution time: " + str(datetime.timedelta(seconds=int(totalTime))))
