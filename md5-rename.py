import os
import re
import sys
import hashlib

md5_pattern = re.compile("^[0123456789abcdefABCDEF]{32,32}(\..+)?$")
keep_existing = False
keep_extensions = False
verbose = False
recursive = False

def get_file_md5(file_path):
	md5 = hashlib.md5()
	file = open(file_path, "r")
	buffer = file.read(1024)
	while len(buffer) > 0:
		md5.update(buffer)
		buffer = file.read(1024)
	return md5.hexdigest()

def process_directory(directory_path):
	item_names = os.listdir(directory_path)
	for item_name in item_names:
		process_item(os.path.join(directory_path, item_name))

def process_item(item_path):
	if os.path.exists(item_path) == True:
		if keep_existing == False or md5_pattern.match(os.path.basename(item_path)) == None:
			if os.path.isdir(item_path) == True:
				if recursive == True:
					if verbose == True:
						print "Decending into directory '" + item_path + "'."
					process_directory(item_path)
				else:
					if verbose == True:
						print "Not decending into directory '" + item_path + "'."
			else:
				md5_name = get_file_md5(item_path)
				md5_path = os.path.join(os.path.dirname(item_path), md5_name)
				if keep_extensions == True:
					md5_path += os.path.splitext(item_path)[1]
				if verbose == True:
					print "Renaming '" + item_path + "'\n      to '" + md5_path + "'."
				os.rename(item_path, md5_path)
		else:
			if verbose == True:
				print "Ignoring '" + item_path + "'."
	else:
		if verbose == True:
			print "Item '" + item_path + "' doesn't exist."

for item_name in sys.argv[1:]:
	if item_name == "--keep-existing":
		keep_existing = True
	elif item_name == "--override-existing":
		keep_existing = False
	elif item_name == "--keep-extensions":
		keep_extensions = True
	elif item_name == "--remove-extensions":
		keep_extensions == False
	elif item_name == "--verbose":
		verbose = True
	elif item_name == "--silent":
		verbose = False
	elif item_name == "--recursive":
		recursive = True
	elif item_name == "--not-recursive":
		recursive = False
	else:
		process_item(os.path.abspath(item_name))
