"""

Author: Corneel den Hartogh
Course: Heuristics

Description: Exporting per type of activity on which day it falls for all good rosters

"""

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


excel_file = "activitySpread.xls"
rosters = 0
activityTypes = {}

# select all rosters that score aboven 1400 from 2 different places
for filename in glob.glob('rosters/*.json'):
	if float(filename.split("_",2)[1]) >= 1400.00:
		rosters += 1
		with open(filename) as jsonfile:
			data = json.load(jsonfile)
			for x in (data["roster"]["activities"]):
				activityType =  x["activity"]["subject"] + " " + x["activity"]["kind"]
				if activityType not in activityTypes.keys():
					activityTypes[activityType] = [x["activity"]["slot"][0]]
				else:
					activityTypes[activityType].append(x["activity"]["slot"][0])

for filename in glob.glob('rosters_server/*.json'):
	if float(filename.split("_",3)[2]) >= 1400.00:
		rosters += 1
		with open(filename) as jsonfile:
			data = json.load(jsonfile)
			for x in (data["roster"]["activities"]):
				activityType =  x["activity"]["subject"] + " " + x["activity"]["kind"]
				activityTypes[activityType].append(x["activity"]["slot"][0])

# get results in excel
rb = open_workbook(excel_file)
wb = copy(rb)
ws = wb.get_sheet(0)
ws.write(0,7,str(rosters) + " rosters above 1400")


row = 1
for key, values in activityTypes.items():
	monday,tuesday,wednesday,thursday,friday = 0,0,0,0,0
	for value in values:
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
	result = [monday, tuesday, wednesday, thursday, friday]

	ws.write(row,7,key)
	ws.write(row,8,result[0])
	ws.write(row,9,result[1])
	ws.write(row,10,result[2])
	ws.write(row,11,result[3])
	ws.write(row,12,result[4])
	row += 1

wb.save(excel_file)


