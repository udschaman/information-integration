import utils.db_utils as util
import utils.scrape_utils as scrape
from urllib.parse import urljoin
import datetime
from timeit import default_timer as timer
from extractors import extractdb

# create table SQL statement
createSightingsTable = "CREATE TABLE IF NOT EXISTS ufosightings(id SERIAL PRIMARY KEY, date_time text, city text, state text, shape text, duration text, summary text, posted text, href text);"

# create table if not exists, set autoincrement to 1 and delete all from the table
util.executeSingleInsertOrCreate(createSightingsTable, extractdb)
util.executeSingleInsertOrCreate("SELECT setval('ufosightings_id_seq', 1)", extractdb)
util.executeSingleInsertOrCreate("DELETE FROM ufosightings", extractdb)

# total number of rows processed
totalRows = 0
# number of links with no tables
errorTables = 0
# number of empty tables
emptyTables = 0
# number of malformed tuples
malformedTuples = 0

# insert query for ufo sightings cases
query = "INSERT INTO ufosightings (date_time, city, state, shape, duration, summary, posted, href) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
# base url
reportsBase = "http://www.nuforc.org/webreports/ndxevent.html"
# table with all cases by event date
table = scrape.getDataTable(reportsBase)

if table == None:
    print("Table could not be found")
else:
    # start measuring time
    start = timer()

    # collect all links from the main table
    links = table.findAll("a")
    print("#links: " + str(len(links)))

    # start scraping data for every link in the main table
    for link in links:
        current = urljoin(reportsBase, link["href"])
        print("number of rows already inserted: " + str(totalRows))
        print("currently processed link: " + current)
        next = timer()
        timeSoFar = next - start
        print("execution time: " + str(datetime.timedelta(seconds=int(timeSoFar))))
        casesTable = scrape.getDataTable(current)
        if casesTable == None:
            print("Table for current cases link could not be found")
            errorTables += 1
        else:
            rows = casesTable.find("tbody").findAll("tr")
            if rows == None:
                print("Table contains no rows")
                emptyTables += 1
            else:
                rowsList = []
                for row in rows:
                    t = ()
                    cells = row.find_all("td")
                    for cell in cells:
                        if cell.get_text():
                            t += (cell.get_text(),)
                        else:
                            t += ("NULL",)

                    t += (urljoin(current, cells[0].find("a")["href"]),)
                    if len(t) == 8:
                        rowsList.append(t)
                    else:
                        malformedTuples += 1
                util.bulkInsert(query, rowsList, extractdb)
                totalRows += len(rowsList)

    end = timer()
    totalTime = end - start
    print("Scraping process is completed.")
    print("Total number of rows processed: " + str(totalRows))
    print("Number of links with no tables: " + str(errorTables))
    print("Number of empty tables: " + str(emptyTables))
    print("number of malformed tuples: " + str(malformedTuples))
    print("Total execution time: " + str(datetime.timedelta(seconds=int(totalTime))))