from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup

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