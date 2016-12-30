import collections
import os
import utils.ui_utils as ui

selected_state = ""
selected_city = ""
selected_shape = ""
selected_airports = ""
selected_date = ""

def return_begin():
	begin = """
		<!DOCTYPE html>
		<html>
			<head>
				<title>UFO sightings</title>
				<meta name="viewport" content="initial-scale=1.0">
				<meta charset="utf-8">
				<style>
					html, body { height: 100%; margin: 0; padding: 0; }
					#map { height: 75%; width: 75%;	}
				</style>
			</head>
		<body>
	"""
	return begin

def return_end():
	end = """
		</body>
		</html>
	"""
	return end


###########################
def return_heatmap():
	heatmap = """
		<h1>Heatmap of all sightings</h1>
	"""
	return heatmap
	
def return_wikipedia():
	city_wiki = """
		<h1>Wikipedia article of the city</h1>
	"""
	return city_wiki

def return_gm():
	lat = ui.get_lat(selected_state, selected_city)
	lon = ui.get_lon(selected_state, selected_city)

	airports = ui.get_airports(selected_airports, lat[0][0], lon[0][0])

	html_airports = ""

	for element in airports:
		html_airports = html_airports + "[\"" + str(element[0]) + "\", " + str(element[1]) + ", " + str(element[2]) + "],"
	
	html_airports = html_airports[:-1]

	show_map = """
		<h1>Google Map of the city with the airports in the choosen area</h1>
		<div id="map"></div>
		<script>
			function initMap() {
				var location = {lat:""" + str(lat[0][0]) + ", lng: " + str(lon[0][0]) + """}
				var map = new google.maps.Map(document.getElementById('map'), {
					center: location,
					zoom: 8,
				   	scaleControl: true
				});
				var marker = new google.maps.Marker({
					position: location,
					map: map,
					title: '""" + selected_city + """'
				});

				var airports = [""" + html_airports + """];

				var marker, i;

				for (i = 0; i < airports.length; i++) {  
					marker = new google.maps.Marker({
						icon: 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png',
						position: new google.maps.LatLng(airports[i][1], airports[i][2]),
						map: map,
						title: airports[i][0]
					});
				}
			}
		</script>
		<script src="https://maps.googleapis.com/maps/api/js?&callback=initMap" 
			async defer></script>
	"""

	return show_map

def return_sightings():
	sightings = """
		<h1>All sightings for the choosen city</h1>
	"""
	return sightings


#######################

def return_results(date):
	global selected_date
	selected_date = date

	result = return_begin() + return_sightings() + return_heatmap() + return_gm() + return_wikipedia() + return_end()
	return result

def return_date(airport):
	global selected_airports
	selected_airports = airport
	
	date = return_begin() + """
		<h1>Select a Date</h1>

		<link rel="stylesheet" href="https://ajax.googleapis.com/ajax/libs/jqueryui/1.11.4/themes/smoothness/jquery-ui.css">
		<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
		<script src="https://ajax.googleapis.com/ajax/libs/jqueryui/1.11.4/jquery-ui.min.js"></script>
		<script>
			$(document).ready(function() { $("#datepicker").datepicker({dateFormat: 'yy-mm-dd'})});
		</script>

		<form method="POST" action="/result">
			<label for="datepicker">Date</label>
			<input name="datepicker" id="datepicker" />
			<br></br>
			<input type="submit" value="send"/>			
		</form>

	""" + return_end()

	return date

def return_states():
	states = ""
	temp_state = ""
	orderedStates =  collections.OrderedDict(sorted(ui.state_dict.items(), key=lambda t: t[1]))
	for element in orderedStates.values():
		temp_state = "<option values=\"" + element + "\">" + element + "</option>" + os.linesep
		states = states + temp_state

	return_value = return_begin() + """
		<h1>Select State</h1>

		<form method="POST" action="/cities">
			<label for="state">States</label>
			<select name="state" id="state">"""+ states + """
			</select>
			<br></br>
			<input type="submit" value="send"/>			
		</form>
	""" + return_end()

	return return_value

def return_cities(state):
	global selected_state
	selected_state = state
	
	cities = return_begin() + """
		<h1>Select City</h1>

		<form method="POST" action="/shapes">
			<label for="city">Cities</label>
			<select name="city" id="city">"""+ ui.get_cities(state) + """
			</select>
			<br></br>
			<input type="submit" value="send"/>			
		</form>
	""" + return_end()

	return cities
	
def return_shapes(city):
	global selected_city
	selected_city = city
	
	shapes = ""
	temp_shape = ""

	for element in sorted(ui.shapes_list):
		temp_shape = "<option values=\"" + element + "\">" + element + "</option>" + os.linesep
		shapes = shapes + temp_shape

	result_shape = return_begin() + """
		<h1>Select Shape</h1>

		<form method="POST" action="/airports">
			<label for="shape">Shapes</label>
			<select name="shape" id="shape">"""+ shapes + """
			</select>
			<br></br>
			<input type="submit" value="send"/>			
		</form>		
	""" + return_end()

	return result_shape

def return_airports(shape):
	global selected_shape
	selected_shape = shape

	airports = ""
	temp_airport = ""
	for element in ui.area_range:
		temp_airport = "<option values=\"" + element + "\">" + element + "</option>" + os.linesep
		airports = airports + temp_airport

	result_airports = return_begin() + """
		<h1>Select range for Airports</h1>

		<form method="POST" action="/date">
			<label for="airport">Airport range</label>
			<select name="airport" id="airport">"""+ airports + """
			</select>
			<br></br>
			<input type="submit" value="send"/>			
		</form>

	""" + return_end()

	return result_airports
