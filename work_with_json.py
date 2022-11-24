import json
from config import JSON_FILE

def json_dump(data):
	with open(JSON_FILE, "w") as write_file:
		json.dump(data, write_file)

def json_load():
	with open(JSON_FILE, "r") as read_file:
		data = json.load(read_file)
	return data