##
# Call arguments: path to csv/dat file, database-name (have to exist), username with write access for db, password for the user    
##
import csv
import sys
import psycopg2


dataset = open(sys.argv[1], 'r')

try:
    conn = psycopg2.connect("dbname=" + sys.argv[2] + " user=" + sys.argv[3] + " host='localhost' password=" + sys.argv[4])
    cursor = conn.cursor();

    query = "CREATE TABLE airports(\"airportID\" TEXT, name TEXT, city TEXT, country TEXT, \"IATAFAA\" VARCHAR(3), \"ICAO\" VARCHAR(4), latitude DOUBLE PRECISION, longitude DOUBLE PRECISION, altitude INTEGER, timezone DOUBLE PRECISION, \"DST\" VARCHAR(1), \"Tz\" TEXT);"

    cursor.execute(query)
    conn.commit()


    reader = csv.reader(dataset)
    for row in reader:

        airportID = row[0]
        name = row[1]
        city = row[2]
        country = row[3]
        IATAFAA = row[4]
        ICAO = row[5]
        latitude = row[6]
        longitude = row[7]
        altitude = row[8]
        timezone = row[9]
        DST = row[10]
        Tz = row[11]
    
        query = "INSERT INTO airports(\"airportID\", name, city, country, \"IATAFAA\", \"ICAO\", latitude, longitude, altitude, timezone, \"DST\", \"Tz\") VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
        
        data = (airportID, name, city, country, IATAFAA, ICAO, latitude, longitude, altitude, timezone, DST, Tz)
    
        cursor.execute(query,data)

    conn.commit()
finally:
    dataset.close()
