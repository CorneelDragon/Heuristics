import random
import copy
import json
import time
import glob
from decimal import Decimal

from csvFilesController import classrooms,subjects,students
from classes import Classroom,Subject,Activity,Student,Roster
import classesImport as ci 
from scoreFunction import getScore
from studentOptimization import studentOptimization
from roomOptimization import roomOptimization

rosters = 0
activityTypes = {}

# select all rosters that score 99% of optimal score (=1360)
for filename in glob.glob('top_rosters/*.json'):
	if float(filename.split("_",3)[2]) >= 1360.00:
		rosters += 1
		monday,tuesday,wednesday,thursday,friday = 0,0,0,0,0
		with open(filename) as jsonfile:
			data = json.load(jsonfile)
			for x in (data["roster"]["activities"]):
				value =  x["activity"]["slot"][0]
				if value == 0:
					monday += 1
				elif value == 1:
					tuesday += 1
				elif value == 2:
					wednesday += 1
				elif value == 3:
					thursday += 1
				elif value == 4:
					friday += 1
			if thursday > 27:
				print (thursday, filename)


for filename in glob.glob('imported_rosters/*.json'):
	if float(filename.split("_",3)[2]) >= 1360.00:
		rosters += 1
		monday,tuesday,wednesday,thursday,friday = 0,0,0,0,0
		with open(filename) as jsonfile:
			data = json.load(jsonfile)
			for x in (data["roster"]["activities"]):
				value =  x["activity"]["slot"][0]
				if value == 0:
					monday += 1
				elif value == 1:
					tuesday += 1
				elif value == 2:
					wednesday += 1
				elif value == 3:
					thursday += 1
				elif value == 4:
					friday += 1
			if thursday > 27:
				print (thursday, filename)
