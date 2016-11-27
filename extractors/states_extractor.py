import json
import psycopg2

def executeSingleQuery(query, connStr):
   try:
      conn = psycopg2.connect(connStr)
      cur = conn.cursor()
      cur.execute(query)
      conn.commit()
   except Exception as e:
      if conn:
         conn.rollback()

      print('Error %s' % e)
      sys.exit(1)

   finally:
      if conn:
         conn.close()


def bulkInsert(query, tuples, connStr):
   try:
      conn = psycopg2.connect(connStr)
      cur = conn.cursor()
      cur.executemany(query, tuples)
      conn.commit()
   except Exception as e:
      if conn:
         conn.rollback()

      print('Error %s' % e)
      sys.exit(1)

   finally:
      if conn:
         conn.close()

connection = "dbname='ufos' user='postgres' host='localhost' password='Freakin666!'"

executeSingleQuery("CREATE TABLE IF NOT EXISTS States(state_id SERIAL PRIMARY KEY, code TEXT, name TEXT);", connection)

executeSingleQuery("DELETE FROM States", connection)

query = "INSERT INTO States (code, name) VALUES (%s, %s)"

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
   bulkInsert(query, rowsList, connection)
   num += len(rowsList)
except Exception as e:
   print(e)
finally:
   print(str(num) + " states inserted in total")
