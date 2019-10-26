"""
Author: Corneel den Hartogh
Course: Heuristics

Description: Make from selected rosters one json for subsequent visualization

"""

import json
import os
import glob

files = []

# Now only the best, imported rosters are set in total.json
# Importing other rosters is the same trick
for filename in glob.glob("imported_rosters/*.json"):
	jsonfile = open(filename, 'r')
	files.append(json.load(jsonfile))

output = open('visuals/visual.json', 'w')
json.dump(files,output, indent=4)
