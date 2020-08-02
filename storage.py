import yaml

#File type specific handling of load/write functions.

#YAML
def load_yaml(filename: str):
	with open(filename, 'r') as fd:
		#Takes the YAML data and turns it into python saving it as "data"
		data=yaml.safe_load(fd)

	#Gives you back "data"
	return data

def write_yaml(filename: str, data):
	try:
		with open(filename, 'w') as fd:
			yaml.dump(data, fd)
		return True
	except (OSError,IOError):
		return False

#This section is reserved for general load/write functions to allow for modularity.

def load(filename: str):
	result = load_yaml(filename)
	#Returns the data that was read from the file
	return result

def write(filename: str, data):
	result = write_yaml(filename, data)
	#This returns true or false based on the success of write_yaml
	return result
