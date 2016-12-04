import utils.db_utils as util

connection = "dbname='postgres' user='postgres' host='localhost' password='123456'"
createUser = "DROP ROLE IF EXISTS infint; CREATE ROLE infint PASSWORD 'infint' NOSUPERUSER CREATEDB NOCREATEROLE INHERIT LOGIN;"

createExtractionDB = "CREATE DATABASE extractdb WITH ENCODING='UTF8' OWNER=infint"
createIntegrationDB = "CREATE DATABASE integratedb WITH ENCODING='UTF8' OWNER=infint"

util.executeSingleInsertOrCreate(createUser, connection)
util.createDatabase(createExtractionDB, connection)
util.createDatabase(createIntegrationDB, connection)

print("Project's user and databases were successfully created")