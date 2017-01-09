import utils.db_utils as util
from integration import integratedb
import operator

def find_duplicates(original_list):
	to_remove = list()

	while(len(original_list) != 0):
		first_lat = original_list[0][0]
		first_lon = original_list[0][1]
		first_element = original_list[0]

		temp_list = set()

		for element in range(1, len(original_list)):


			if(first_lat == original_list[element][0] and first_lon == original_list[element][1] and not any(original_list[element] in e for e in to_remove)):
				temp_list.add(original_list[element])
				temp_list.add(first_element)
		original_list.pop(0)
		if(len(temp_list) != 0):
			to_remove.append(list(temp_list))

	for list_element in to_remove:
		temp_remove = list_element[0]
		temp_length = len(list_element[0][2])
		
		for element in list_element:
			if(len(element[2]) > temp_length):
				temp_remove = element
				temp_length = len(element[2])
		
		list_element.remove(temp_remove)
	return to_remove


airports_to_remove = [[] for x in range(9)]
remove_list = list()

airports = util.executeSelect("SELECT lat, lon, airport_name, airport_id FROM airports;", integratedb)
sort_airports = sorted(airports)

delete_statement = "DELETE FROM airports WHERE airport_id in ("


for element in sort_airports:
	if(element[0] < 0 or element[0] > 90):
		delete_statement += str(element[3]) + ", "
	elif(element[0] < 10):
		airports_to_remove[0].append(element)
	elif(element[0] < 20):
		airports_to_remove[1].append(element)
	elif(element[0] < 30):
		airports_to_remove[2].append(element)
	elif(element[0] < 40):
		airports_to_remove[3].append(element)
	elif(element[0] < 50):
		airports_to_remove[4].append(element)
	elif(element[0] < 60):
		airports_to_remove[5].append(element)
	elif(element[0] < 70):
		airports_to_remove[6].append(element)
	elif(element[0] < 80):
		airports_to_remove[7].append(element)
	elif(element[0] <= 90):
		airports_to_remove[8].append(element)
	
for i in range(0, len(airports_to_remove)):
	remove_list.append(find_duplicates(airports_to_remove[i]))

for elements in remove_list:
	if(len(elements) != 0):
		for element in elements:
			for e in element:
				delete_statement += str(e[3]) + ", "

delete_statement = delete_statement[:-2]
delete_statement += ")"

util.executeSingleInsertOrCreate(delete_statement, integratedb)