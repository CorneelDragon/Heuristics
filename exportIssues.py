import random
import copy
import json
import time
import glob
import operator
from decimal import Decimal

from csvFilesController import classrooms,subjects,students
from classes import Classroom,Subject,Activity,Student,Roster
import classesImport as ci 
from scoreFunction import getScore
from studentOptimization import studentOptimization
from roomOptimization import roomOptimization

startTime = time.process_time()
issues = []
num = 0

for filename in glob.glob('imported_rosters/*.json'):
	num += 1
	with open(filename) as jsonfile:
		data = json.load(jsonfile)
		for x in (data["roster"]["issues"]):
			issues.append(x["reference"])

issueDict ={}
issuesUnique = set(issues)

for issueUnique in issuesUnique:
	i = 0
	for issue in issues:
		if issueUnique == issue:
			i += 1
	issueDict[issueUnique] = i 

sorted_issues = sorted(issueDict.items(), key=operator.itemgetter(1), reverse=True)

for sorted_issue in sorted_issues:
	print(sorted_issue)

print("issues: ", len(sorted_issues))
print("rosters: ", num)
