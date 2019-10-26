"""

Author: Corneel den Hartogh
Course: Heuristics

Description: Importing roster and trying to improve them further

"""

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

# select top rosters
for filename in sorted(glob.glob('top_rosters/*.json'), key=lambda x: float(x.split("_",3)[2]), reverse=True):

	startTime = time.process_time()

	bestRoster = ci.Roster(classrooms,subjects, students)
	subject_dct = {x.__str__(): x for x in bestRoster.subjects}
	student_dct = {x.__str__(): x for x in bestRoster.students}

	activities = []

	with open(filename) as jsonfile:
		data = json.load(jsonfile)
		for x in (data["roster"]["activities"]):
				activity = []
				#activity.append(x["activity"]["subject"])
				activity.append(subject_dct[x["activity"]["subject"]])
				activity.append(x["activity"]["kind"])
				activity.append(x["activity"]["lecture_number"])
				activity.append(x["activity"]["group"])
				activity.append(x["activity"]["slot"])
				activity.append(x["activity"]["maxStud"])

				studentsActivity = []

				for student in x["activity"]["students"]:
					if student[-8:][0] == " ":
						studentsActivity.append(student_dct[student[-7:]])
					elif student[-7:][0] == " ":
						studentsActivity.append(student_dct[student[-6:]])
						test = student_dct[student[-6:]]
					else:
						studentsActivity.append(student_dct[student[-8:]])

				activity.append(studentsActivity)
				activities.append(activity)


	bestRoster.activities = [ci.Activity(x[0], x[1], x[2], x[3], x[4], x[5], x[6]) for x in activities]

	for activity in bestRoster.activities:
		activity.assignActivitiesToSubject(bestRoster)

	bestRoster.timetable = {}
	for activity in bestRoster.activities:
	    bestRoster.timetable[activity.slot] = activity

	bestScore = getScore(bestRoster)

	scores = []
	scores.append(bestScore)


    # after a cycle we see if progress has been made, if so, execute whole cycle with new timetable
	while len(scores) == 1 or scores[-1] > scores[-2]:

		# we test every possible switch between slots from the current timetable (this could be done more sophisticated)
		# now it takes 145^2 iterations while it only needs to be 145!
		for x in range(5):
			for y in range(5):
				for z in range(len(classrooms)):
					for x2 in range(5):
						for y2 in range(5):
							for z2 in range (len(classrooms)):

								newRoster = Roster(classrooms,subjects,students)
								newRoster = Roster.duplicateRoster(newRoster,bestRoster)

								slotOne = (x,y,z)
								slotTwo = (x2,y2, z2)

								slots = [slotOne, slotTwo]
								activities = []

								#swap the activities (if any) of two slots
								for index, slot in enumerate(slots):
									if slot in newRoster.timetable:
										activities.append(newRoster.timetable[slot])
									else:
										activities.append(None)

								for i, activity in enumerate(activities):
									for j, slot in enumerate(slots):
										if i != j:
											if activity is not None:
												newRoster.timetable[slot] = activity
												activity.slot = slot
											else:
												if activities[j] is not None:
													del newRoster.timetable[slot]

								# make sure students are sorted appropriately over the WorkLectures and Practica
								# get the timeslots (first 2 values of slot) of the activities and keep only the one's that are double rostered
								newRoster = studentOptimization(newRoster)
								#oldScore = getScore(newRoster)
								newRoster = roomOptimization(newRoster)
								score = getScore(newRoster)
								if score > bestScore:
									bestRoster = newRoster
									bestScore = score



		scores.append(bestScore)

	runtime = time.process_time() - startTime
	bestRoster.exportRoster("imported_rosters/imported",bestScore,runtime)
