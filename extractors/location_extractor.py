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

    query = "CREATE TABLE locations(\"RecordNumber\" INTEGER, \"Zipcode\" INTEGER, \"ZipCodeType\" TEXT, \"City\" TEXT, \"State\" VARCHAR(2), \"LocationType\" TEXT, \"Lat\" DOUBLE PRECISION, \"Long\" DOUBLE PRECISION, \"Xaxis\" TEXT, \"Yaxis\" TEXT, \"Zaxis\" TEXT, \"WorldRegion\" TEXT, \"Country\" TEXT, \"LocationText\" TEXT, \"Location\" TEXT, \"Decommisioned\" TEXT, \"TaxReturnsFiled\" TEXT, \"EstimatedPopulation\" TEXT, \"TotalWages\" TEXT, \"Notes\" TEXT);"

    cursor.execute(query)
    conn.commit()

    reader = csv.reader(dataset)
    next(reader)
    
    for row in reader:
        RecordNumber = row[0]
        Zipcode = row[1]
        ZipCodeType = row[2]
        City = row[3]
        State = row[4]
        LocationType = row[5]
        if not row[6]:
            Lat = None
        else:
            Lat = row[6]
        if not row[7]:
            Long = None
        else:
            Long = row[7]
        Xaxis = row[8]
        Yaxis = row[9]
        Zaxis = row[10]
        WorldRegion = row[11]
        Country = row[12]
        LocationText = row[13]
        Location = row[14]
        Decommisioned = row[15]
        TaxReturnsFiled = row[16]
        EstimatedPopulation = row[17]
        TotalWages = row[18]
        Notes = row[19]

        query = "INSERT INTO locations(\"RecordNumber\", \"Zipcode\", \"ZipCodeType\", \"City\", \"State\", \"LocationType\", \"Lat\", \"Long\", \"Xaxis\", \"Yaxis\", \"Zaxis\", \"WorldRegion\", \"Country\", \"LocationText\", \"Location\", \"Decommisioned\", \"TaxReturnsFiled\", \"EstimatedPopulation\", \"TotalWages\", \"Notes\") VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"

        data = (RecordNumber, Zipcode, ZipCodeType, City, State, LocationType, Lat, Long, Xaxis, Yaxis, Zaxis, WorldRegion, Country, LocationText, Location, Decommisioned, TaxReturnsFiled, EstimatedPopulation, TotalWages, Notes)

        cursor.execute(query,data)

    conn.commit()

finally:
    dataset.close()

