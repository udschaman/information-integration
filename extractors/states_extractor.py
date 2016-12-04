import json
import utils.db_utils as util
from extractors import extractdb

util.executeSingleInsertOrCreate("CREATE TABLE IF NOT EXISTS states(state_id SERIAL PRIMARY KEY, code TEXT, name TEXT);", extractdb)

util.executeSingleInsertOrCreate("SELECT setval('states_state_id_seq', 1)", extractdb)
util.executeSingleInsertOrCreate("DELETE FROM states", extractdb)

query = "INSERT INTO states (code, name) VALUES (%s, %s)"

try:
   num = 0
   with open('../sources/states.json', encoding='utf-8') as data_file:
      data = json.loads(data_file.read())
      data_file.close()
   rowsList = []
   for key, value in data.items():
      t = ()
      t += (key,)
      t += (value,)
      rowsList.append(t)
   util.bulkInsert(query, rowsList, extractdb)
   num += len(rowsList)
except Exception as e:
   print(e)
finally:
   print(str(num) + " states inserted in total")
