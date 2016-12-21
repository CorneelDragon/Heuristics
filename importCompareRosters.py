# import roster x and save type and timetable
# save empty spots as well
# 
# compare with other rosters, check if roster is same type
# get also the empty spots out of other rosters
#
#

import random
import copy
import json
import time
import glob
from decimal import Decimal
from xlrd import *
from xlwt import *
from xlutils.copy import copy

from csvFilesController import classrooms,subjects,students
from classes import Classroom,Subject,Activity,Student,Roster
import classesImport as ci 
from scoreFunction import getScore
from studentOptimization import studentOptimization
from roomOptimization import roomOptimization

rosterList = []

hillclimber = []
annealing = []
genetics = []
top = 0

#instead of activitiesDict just a list
def buildDict(data, x, y, z, activitiesDict):
	for activity in (data["roster"]["activities"]):
		if [x,y,z] == activity["activity"]["slot"]:
			activitiesDict[(x,y,z)] = activity["activity"]["subject"] + " " + \
			activity["activity"]["kind"]
	if (x,y,z) not in activitiesDict:
		activitiesDict[(x,y,z)] = "empty"
	return activitiesDict

def saveRoster(filename, hillclimber, annealing, genetics):
	kind = None
	topBool = False
	if filename.split("/")[1][:11] == "hillclimber":
		kind = "hillclimber"
		hillclimber.append(filename)
	elif filename.split("/")[1][:9] == "annealing":
		kind = "annealing"
		annealing.append(filename)
	elif filename.split("/")[1][:8] == "genetics":
		kind = "genetics"
		genetics.append(filename)

	with open(filename) as jsonfile:
		data = json.load(jsonfile)
		activitiesDict = {}
		for x in range(5):
			for y in range (5):
				if y == 4:
					z = 5
					activitiesDict = buildDict(data, x, y, z, activitiesDict)
				else:
					for z in range(7):
						activitiesDict = buildDict(data, x, y, z, activitiesDict)
	return [filename, activitiesDict, kind, topBool]

# select all rosters that score 99% of optimal score (=1360)
for filename in glob.glob('rosters/*.json'):
	if float(filename.split("_",2)[1]) >= 1400.00:
		topBool = True
		top += 1
	rosterList.append(saveRoster(filename, hillclimber, annealing, genetics))
	#osterList.append([filename, activitiesDict, kind, topBool])

for filename in glob.glob('rosters_server/*.json'):
	if float(filename.split("_",3)[2]) >= 1400.00:
		topBool = True
		top += 1
	rosterList.append(saveRoster(filename, hillclimber, annealing, genetics))
	#osterList.append([filename, activitiesDict, kind, topBool])

for roster in rosterList:
	timetable = roster[1]
	for roster in rosterList:


"""
print(len(rosterList))
print("HC: ", len(hillclimber))
print("SA: ", len(annealing))
print("GA:", len(genetics))
print("top: ", top)
for x in range(5):
	for y in range (5):
		for z in range(7):
			for key,value in rosterList[0][1].items():
				if (x,y,z) == key:
					print (key, value)
"""