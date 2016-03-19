import json
import os

def get_full_file_path(file_name):
	return 'store/' + file_name

def write_json_data(json_data, file_name):
	full_file_path = get_full_file_path(file_name)
	with open(full_file_path, 'w') as file:
		json.dump(json_data, file)

def get_json_data(file_name):
	full_file_path = get_full_file_path(file_name)

	if not os.path.exists(full_file_path):
		write_json_data({}, file_name)

	with open(full_file_path, 'r') as file:
		return json.load(file)

def update_data(json_data, file_name="top100.json"):
	old_data = get_json_data(file_name)
	new_data = {}
	for key in json_data:
		if key not in old_data:
			new_data[key] = json_data[key]
	write_json_data(json_data, file_name)
	return new_data
