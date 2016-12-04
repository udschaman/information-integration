import utils.db_utils as util
from integration import integratedb
from extractors import extractdb

util.executeSingleInsertOrCreate("CREATE TABLE IF NOT EXISTS states(state_id SERIAL PRIMARY KEY, state_code TEXT, state_name TEXT);", integratedb)

util.executeSingleInsertOrCreate("SELECT setval('states_state_id_seq', 1)", integratedb)
util.executeSingleInsertOrCreate("DELETE FROM states", integratedb)

statesList = util.executeSelect("SELECT code, name from states order by code", extractdb)

insertStates = "INSERT INTO states (state_code, state_name) VALUES (%s, %s)"

util.bulkInsert(insertStates, statesList, integratedb)

print("States were successfully copied into the integrated database")
