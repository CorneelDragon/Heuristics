from scoreFunction import prepareSubjectScore

def reproduceTimeOrDay(timetable, day, timeSlot, first, second, activities, roomAmount):

	split = day + timeSlot

	for recombine in range(4):
		if recombine == 0 or recombine == 2:
			start = 0
			end = split
		else:
			start = split
			end = 5
		if recombine == 0 or recombine == 3:
			parentTimetable = first.timetable
		else: 
			parentTimetable = second.timetable

		if day == 0:
			startDay = 0
			endDay = 5
			startTimeSlot = start
			endTimeSlot = end
		else:
			startDay = start
			endDay = end
			startTimeSlot = 0
			endTimeSlot = 5
        
		for x in range(startDay, endDay):
			for y in range (startTimeSlot, endTimeSlot):
				for z in range(roomAmount):
					if(x,y,z) in parentTimetable and (x,y,z) not in timetable.keys() and parentTimetable[(x,y,z)] not in timetable.values():
						for activity in activities:
							if activity == parentTimetable[(x,y,z)]:
								timetable[(x,y,z)] = activity
								activity.slot = (x,y,z)
	return [timetable, activities]

def reproduceSubjects(timetable, first, second, activities, roomAmount):

	first.subjectsLargeStart = sorted(first.subjects, key=lambda x:len(x.activities), reverse = True)
	second.subjectsLargeStart = sorted(second.subjects, key=lambda x:len(x.activities), reverse = True)

	for x in range(len(first.subjects)):
		firstResult =  prepareSubjectScore(first.subjectsLargeStart[x])
		secondResult = prepareSubjectScore(second.subjectsLargeStart[x])
		if sum(firstResult) > sum(secondResult):
			bestSubject = first.subjectsLargeStart[x]
			repairSubject = second.subjectsLargeStart[x]
		else: 
			bestSubject = second.subjectsLargeStart[x]
			repairSubject = first.subjectsLargeStart[x]

		for activityBest in bestSubject.activities:
			if activityBest.slot not in timetable.keys():
				for activity in activities:
					if activity == activityBest:
						timetable[activityBest.slot] = activity
						activity.slot = activityBest.slot 
			else:
				for activityRepair in repairSubject.activities:
					if activityBest == activityRepair:
						if activityRepair.slot not in timetable.keys():
							for activity in activities:
								if activity == activityRepair:
									timetable[activityRepair.slot] = activity
									activity.slot = activityRepair.slot 

	return [timetable, activities]
