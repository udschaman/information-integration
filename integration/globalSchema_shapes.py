import utils.db_utils as util
from integration import integratedb
from extractors import extractdb

util.executeSingleInsertOrCreate("CREATE TABLE IF NOT EXISTS shapes(shape_id SERIAL PRIMARY KEY, shape_name TEXT);", integratedb)

util.executeSingleInsertOrCreate("SELECT setval('shapes_shape_id_seq', 1)", integratedb)
util.executeSingleInsertOrCreate("DELETE FROM shapes", integratedb)

shapesList = util.executeSelect("SELECT DISTINCT lower(shape) AS shape FROM ufosightings ORDER BY shape", extractdb)

insertStates = "INSERT INTO shapes (shape_name) VALUES (%s)"

util.bulkInsert(insertStates, shapesList, integratedb)

print("Shapes (uncleaned) were successfully copied into the integrated database")
