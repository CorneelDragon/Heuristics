import json
import os
import glob

files = []

# Now only the best, imported rosters are set in total.json
for filename in glob.glob("imported_rosters/*.json"):
	jsonfile = open(filename, 'r')
	files.append(json.load(jsonfile))

output = open('total.json', 'w')
json.dump(files,output, indent=4)