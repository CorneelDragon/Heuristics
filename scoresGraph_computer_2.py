"""

Author: Corneel den Hartogh
Course: Heuristics

Description: Export scores to excel on pc 1

"""

import json
import glob
import random

from xlrd import *
from xlwt import *
from xlutils.copy import copy

excel_file = "scoresGraph_computer_2.xls"

hillclimber = []
annealing = []
genetics = []

for filename in glob.glob("rosters_computer_2/*.json"):
	score = filename.split("_",5)[3]
	time = filename.split("_",5)[4]

	if filename.split("/")[1][:11] == "hillclimber":
		hillclimber.append([score,time])
	elif filename.split("/")[1][:9] == "annealing":
		annealing.append([score,time])
	elif filename.split("/")[1][:8] == "genetics":
		genetics.append([score,time])

# select randomly 70 results per algorithm
hillclimber = random.sample(hillclimber, 70)
annealing = random.sample(annealing, 70)
genetics = random.sample(genetics, 70)

# get arrays in excel
rb = open_workbook(excel_file)
wb = copy(rb)
ws = wb.get_sheet(0)

row = 1
for values in hillclimber:
	ws.write(row,0,values[1])
	ws.write(row,1,values[0])
	row += 1

row = 1
for values in annealing:
	ws.write(row,2,values[1])
	ws.write(row,3,values[0])
	row += 1

row = 1
for values in genetics:
	ws.write(row,4,values[1])
	ws.write(row,5,values[0])
	row += 1

wb.save(excel_file)
