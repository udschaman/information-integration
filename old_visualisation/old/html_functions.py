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
					#map { height: 75%; width: 100%;	}
					table { width:  100%; border-collapse: collapse; }
        			td, th { border: 1px solid black; }
        			.scrollingTable { width: 100%; overflow-y: auto; }
				</style>
			</head>
		<body onload="makeTableScroll();">
	"""
	return begin

def return_end():
	end = """
		</body>
		</html>
	"""
	return end


###########################	
def return_wikipedia():
	city_wiki = """
		<h1>Wikipedia article of the city</h1>
	"""
	return city_wiki

#######################

def return_sightings():
	db_sightings = ui.get_sightings(selected_date, selected_city, selected_state, selected_shape)

	web_sightings = ""
	for element in db_sightings:

		if("*" in selected_date):
			web_date = "<td>" + str(element[3])  + "</td>"
		else:
			web_date = "<td>" + selected_date  + "</td>"

		web_city = "<td>" + selected_city + "</td>"
		web_state = "<td>" + selected_state + "</td>"
		
		if("*" in selected_shape):
			web_shape = "<td>" + element[-1]  + "</td>"
		else:
			web_shape = "<td>" + selected_shape  + "</td>"

		web_duration = "<td>" + element[0]  + "</td>"
		web_summary = "<td>" + element[1] + "</td>"
		web_link = "<td>" + element[2] + "</td>"


		web_sightings = web_sightings + "<tr>" + web_date + web_city + web_state + web_shape + web_duration + web_summary + web_link + "</tr>"

	sightings = """
		<h1>All """ + str(len(db_sightings)) + """ sightings for """ + selected_city + """, """ + selected_state + """</h1>
		<script type="text/javascript">
	        function makeTableScroll() {
	            var maxRows = 25;

	            var table = document.getElementById('myTable');
	            var wrapper = table.parentNode;
	            var rowsInTable = table.rows.length;
	            var height = 0;
	            if (rowsInTable > maxRows) {
	                for (var i = 0; i < maxRows; i++) {
	                    height += table.rows[i].clientHeight;
	                }
	                wrapper.style.height = height + "px";
	            }
	        }
    	</script>
	    <div class="scrollingTable">
	        <table id="myTable">
	            <tr>
	                <th>Date</th>
	                <th>City</th>
	                <th>State</th>
	                <th>Shape</th>
	                <th>Duration</th>
	                <th>Summary</th>
	                <th>Link</th>
	            </tr>""" + web_sightings + """	            
	        </table>
	    </div>
	"""
	return sightings

def return_gm():
	lat = ui.get_lat(selected_state, selected_city)
	lon = ui.get_lon(selected_state, selected_city)

	airports = ui.get_airports(selected_airports, lat[0][0], lon[0][0])
	all_lat_lon = ui.get_all_lat_lon()

	heatmap_elements = ""

	for element in all_lat_lon:
		heatmap_elements = heatmap_elements + "{location: new google.maps.LatLng(" + str(element[0]) + ", " + str(element[1]) + "), weight: " + str(element[2]) + "},"

	heatmap_elements = heatmap_elements[:-1]

	html_airports = ""
	for element in airports:
		html_airports = html_airports + "[\"" + str(element[0]) + "\", " + str(element[1]) + ", " + str(element[2]) + "],"
	
	html_airports = html_airports[:-1]

	show_map = """
		<h1>Heatmap for all sightings and the map for """ + selected_city + """,""" + selected_state + """ and the airports in the area</h1>
		<div id="map"></div>
		<script>
			function initMap() {
				var location = {lat:""" + str(lat[0][0]) + ", lng: " + str(lon[0][0]) + """}
				var map = new google.maps.Map(document.getElementById('map'), {
					center: location,
					zoom: 8,
				   	scaleControl: true
				});

				var heatmap = new google.maps.visualization.HeatmapLayer({
            		data: getPoints(),
            		map: map,
            		radius : 20
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

			function getPoints() {
          		return [ """ + heatmap_elements + """  ];
        	}
		</script>
		<script src="https://maps.googleapis.com/maps/api/js?libraries=visualization&callback=initMap" 
			async defer></script>
	"""

	return show_map

def return_results(date):
	global selected_date
	selected_date = date

	result = return_begin() + return_sightings() + return_gm() + return_wikipedia() + return_end()
	return result

def return_date(airport):
	global selected_airports
	selected_airports = airport
	
	date = return_begin() + """
		<h1>Select a Date or leave empty for all Dates</h1>

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
