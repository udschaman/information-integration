import utils.db_utils as util
from integration import integratedb
from extractors import extractdb

util.executeSingleInsertOrCreate("CREATE TABLE IF NOT EXISTS airports(airport_id SERIAL PRIMARY KEY, airport_name TEXT, lat REAL, lon REAL);", integratedb)

util.executeSingleInsertOrCreate("SELECT setval('airports_airport_id_seq', 1)", integratedb)
util.executeSingleInsertOrCreate("DELETE FROM airports", integratedb)

airportList = util.executeSelect("SELECT DISTINCT lower(name) AS name, latitude, longitude FROM airports WHERE country = 'United States' ORDER BY name", extractdb)

insertAirports = "INSERT INTO airports (airport_name, lat, lon) VALUES (%s, %s, %s)"

util.bulkInsert(insertAirports, airportList, integratedb)

print("Airports were successfully copied into the integrated database")
