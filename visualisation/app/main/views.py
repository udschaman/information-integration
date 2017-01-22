from flask import render_template, redirect, url_for, session, request, current_app, escape, jsonify
from . import main
import sys
import time
import fileinput
import os

heatmap_dir = os.path.abspath(os.path.dirname(__file__))
heatmap_dir = heatmap_dir[:-4] + "templates/site_elements/heatmap.html"

shape_data_dir = os.path.abspath(os.path.dirname(__file__))
shape_data_dir = shape_data_dir[:-4] + "static/js/plugins/morris/shape-data.js"

state_data_dir = os.path.abspath(os.path.dirname(__file__))
state_data_dir = state_data_dir[:-4] + "static/js/plugins/morris/state-data.js"

date_data_dir = os.path.abspath(os.path.dirname(__file__))
date_data_dir = date_data_dir[:-4] + "static/js/plugins/morris/date-data.js"

basedir = os.path.abspath(os.path.dirname(__file__))
basedir = basedir[:-23]
sys.path.append(basedir)
import utils.ui_utils as ui


index_loadedData = False
heatmap_elements = ""


@main.route('/index.html', methods=['GET', 'POST'])
@main.route('/', methods=['GET', 'POST'])
def index():
	global index_loadedData
	global heatmap_elements
	
	if request.method == 'GET':
		if(index_loadedData == False):
			#create heatmap data
			heatmap_elements = ui.get_heatmap_elements()

			#create shapes bar chart data
			shape_elements = ui.get_shape_count()
			with fileinput.FileInput(shape_data_dir, inplace=True, backup='.bak') as file:
				for line in file:
					print(line.replace("[]", "[" + shape_elements + "]"), end='')

			#create states bar chart data
			state_elements = ui.get_state_count()
			with fileinput.FileInput(state_data_dir, inplace=True, backup='.bak') as file:
				for line in file:
					print(line.replace("[]", "[" + state_elements + "]"), end='')

			#create date line chart data
			date_elements = ui.get_date_count()
			with fileinput.FileInput(date_data_dir, inplace=True, backup='.bak') as file:
				for line in file:
					print(line.replace("[]", "[" + date_elements + "]"), end='')

			index_loadedData = True

		return render_template('index.html', heatmap_values=heatmap_elements)

@main.route('/tables.html', methods=['GET', 'POST'])
def tables():

	state_selection = ui.get_states()

	if request.method == 'GET':
		return render_template('tables.html', state_selection=state_selection)
	if request.method == 'POST':
		state = str(escape(request.form['state']))
		states = ui.get_state_sightings(state)
		amount_sightings = len(states)

		return render_template('tables.html', state_value=state, state_selection=state_selection, states=states, amount_sightings=amount_sightings)	

