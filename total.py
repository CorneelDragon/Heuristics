import json
import os
import glob

files = []

for filename in glob.glob("rosters/*.json"):
	jsonfile = open(filename, 'r')
	files.append(json.load(jsonfile))

output = open('total.json', 'w')
json.dump(files,output, indent=4)