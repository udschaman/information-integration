#!pip3 install beautifulsoup4
#!pip3 install psycopg2
from urllib.request import urlopen
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import psycopg2
import csv
import json

def getDataTable(url):
    try:
        html = urlopen(url)
    except HTTPError as e:
        return None
    try:
        bsObj = BeautifulSoup(html.read(), "html.parser")
        table = bsObj.find("table")
    except AttributeError as e:
        return None
    return table
  
def executeSingleQuery(query):
    try:
        conn = psycopg2.connect("dbname='infint' user='user' host='localhost' password='123456'")
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
            
def bulkInsert(query, tuples):
    try:
        conn = psycopg2.connect("dbname='infint' user='user' host='localhost' password='123456'")
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
            
executeSingleQuery("CREATE TABLE IF NOT EXISTS ScrapedData(id SERIAL PRIMARY KEY, date_time text, city text, state text, shape text, duration text, summary text, posted text, href text);")

executeSingleQuery("DELETE FROM ScrapedData")

totalRows = 0
errorTables = 0
emptyTables = 0
malformedTuples = 0
query = "INSERT INTO ScrapedData (date_time, city, state, shape, duration, summary, posted, href) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
reportsBase = "http://www.nuforc.org/webreports/ndxevent.html"
table = getDataTable(reportsBase)
if table == None:
    print("Table could not be found")
else:
    links = table.findAll("a")
    print("#links: " + str(len(links)))
    for link in links:
        current = urljoin(reportsBase, link["href"])
        print("total number of rows inserted: " + str(totalRows))
        print("currently processed link: " + current)
        
        casesTable = getDataTable(current)
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
                        #print(t)
                    else:
                        malformedTuples += 1
                bulkInsert(query, rowsList)
                totalRows += len(rowsList)
                
                #print(rowsList)
                    
                #cur.executemany(query, rowsList)
