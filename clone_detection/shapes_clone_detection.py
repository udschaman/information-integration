import utils.db_utils as util
from integration import integratedb
import operator
from itertools import groupby
import Levenshtein


other_id = util.executeSelect("SELECT shape_id FROM shapes WHERE shape_name = \'other\';", integratedb)[0][0]
unknown_id = util.executeSelect("SELECT shape_id FROM shapes WHERE shape_name = \'unknown\';", integratedb)[0][0]
null_id = util.executeSelect("SELECT shape_id FROM shapes WHERE shape_name = \'null\';", integratedb)[0][0]

util.executeSingleInsertOrCreate("UPDATE ufosightings SET shape_id = " + str(other_id) + " WHERE shape_id in (" + str(unknown_id) + ", " + str(null_id) + ")", integratedb)
util.executeSingleInsertOrCreate("DELETE FROM shapes WHERE shape_id in (" + str(unknown_id) + ", " + str(null_id) + ")", integratedb)

shapes = util.executeSelect("SELECT shape_name, shape_id FROM shapes;", integratedb)

sorted_shapes = list()
shapes_to_update = list()

for element in sorted(shapes):
	sorted_shapes.append(element[0])

named_list = [[] for x in range(26)]

counter = 0
for letter, words in groupby(sorted_shapes, key=operator.itemgetter(0)):
	letter_list = list()
	for word in words:
		letter_list.append(word)
	named_list[counter].append(letter_list)
	counter += 1

for elements in named_list:
	if(len(elements) != 0):
		for element in elements[0]:
			first_element = element
			highest_similarity = 0
			highest_element = ""
			sim_list = set()

			for e in range(0, len(elements[0])):
				temp_sim = Levenshtein.ratio(first_element, elements[0][e])
				if(temp_sim != 1 and temp_sim > highest_similarity):
					highest_similarity = temp_sim
					highest_element = elements[0][e]

			if(highest_similarity > 0.65):
				sim_list.add(first_element)
				sim_list.add(highest_element)
			if(len(sim_list) != 0 and sim_list not in shapes_to_update):
				shapes_to_update.append(sim_list)


name_id_list = list()

for elements in shapes_to_update:
	temp_set = set()
	for element in elements:
		for e in sorted(shapes):
			if(element in e):
				temp_set.add(e)
	name_id_list.append(temp_set)

for element in name_id_list:
	util.executeSingleInsertOrCreate("UPDATE ufosightings SET shape_id = " + str(list(element)[0][1]) + " WHERE shape_id in (" + str(list(element)[1][1]) + ")", integratedb)
	util.executeSingleInsertOrCreate("DELETE FROM shapes WHERE shape_id in (" + str((list(element)[1][1])) + ")", integratedb)
