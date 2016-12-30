import utils.db_utils as db_util
from integration import integratedb
import os

def get_cities(state_name):
	state_id = db_util.executeSelect("SELECT state_id FROM states WHERE state_name = '" + state_name + "'", integratedb)[0][0]
	cities = db_util.executeSelect("SELECT city_name FROM cities WHERE state_id = " + str(state_id) + " ORDER BY city_name", integratedb)
	
	city = ""
	return_cities = ""
	for element in cities:
		city = "<option values=\"" + element[0] + "\">" + element[0] + "</option>" + os.linesep
		return_cities = return_cities + city

	return return_cities	

def get_lat(state, city):
	state_id = db_util.executeSelect("SELECT state_id FROM states WHERE state_name = '" + state + "'", integratedb)[0][0]
	lat = db_util.executeSelect("SELECT lat FROM cities WHERE state_id = " + str(state_id) + " AND city_name = '" + str(city) + "'", integratedb)

	return lat

def get_lon(state, city):
	state_id = db_util.executeSelect("SELECT state_id FROM states WHERE state_name = '" + state + "'", integratedb)[0][0]
	lon = db_util.executeSelect("SELECT lon FROM cities WHERE state_id = " + str(state_id) + " AND city_name = '" + str(city) + "'", integratedb)

	return lon

def get_airports(area, lat, lon):
	
	if(area == "*"):
		airports = db_util.executeSelect("SELECT airport_name, lat, lon FROM airports", integratedb)		
	else:
		area = int(area) / 100
		airports = db_util.executeSelect("SELECT airport_name, lat, lon FROM airports WHERE lat >= " + str(lat - area) + " AND lat <= " + str(lat + area) + " AND lon >= " + str(lon - area) + " AND lon <= " + str(lon + area) , integratedb)

	return airports
	


state_dict = {"AL" : "Alabama",
    "AK" : "Alaska",
    "AS" : "American Samoa",
    "AZ" : "Arizona",
    "AR" : "Arkansas",
    "CA" : "California",
    "CO" : "Colorado",
    "CT" : "Connecticut",
    "DE" : "Delaware",
    "DC" : "District Of Columbia",
    "FM" : "Federated States Of Micronesia",
    "FL" : "Florida",
    "GA" : "Georgia",
    "GU" : "Guam",
    "HI" : "Hawaii",
    "ID" : "Idaho",
    "IL" : "Illinois",
    "IN" : "Indiana",
    "IA" : "Iowa",
    "KS" : "Kansas",
    "KY" : "Kentucky",
    "LA" : "Louisiana",
    "ME" : "Maine",
    "MH" : "Marshall Islands",
    "MD" : "Maryland",
    "MA" : "Massachusetts",
    "MI" : "Michigan",
    "MN" : "Minnesota",
    "MS" : "Mississippi",
    "MO" : "Missouri",
    "MT" : "Montana",
    "NE" : "Nebraska",
    "NV" : "Nevada",
    "NH" : "New Hampshire",
    "NJ" : "New Jersey",
    "NM" : "New Mexico",
    "NY" : "New York",
    "NC" : "North Carolina",
    "ND" : "North Dakota",
    "MP" : "Northern Mariana Islands",
    "OH" : "Ohio",
    "OK" : "Oklahoma",
    "OR" : "Oregon",
    "PW" : "Palau",
    "PA" : "Pennsylvania",
    "PR" : "Puerto Rico",
    "RI" : "Rhode Island",
    "SC" : "South Carolina",
    "SD" : "South Dakota",
    "TN" : "Tennessee",
    "TX" : "Texas",
    "UT" : "Utah",
    "VT" : "Vermont",
    "VI" : "Virgin Islands",
    "VA" : "Virginia",
    "WA" : "Washington",
    "WV" : "West Virginia",
    "WY" : "Wyoming"}

shapes_list = [
"changing", 
"chevron", 
"cigar", 
"circle", 
"cone", 
"crescent", 
"cross", 
"cylinder", 
"delta", 
"diamond", 
"disk", 
"dome", 
"egg", 
"fireball", 
"flare", 
"flash", 
"formation", 
"hexagon", 
"light", 
"oval", 
"pyramid", 
"rectangle", 
"round", 
"sphere", 
"teardrop", 
"triangle", 
"other",
"*"]

area_range = ["0", "10", "25", "50", "75", "100", "150", "300", "500", "*"]