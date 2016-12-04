from decimal import Decimal

def getScore(roster):

	timetable = roster.timetable
	activities = roster.activities
	students = roster.students
	subjects = roster.subjects
	classrooms = roster.classrooms


	# Every timetable is 'valid' so the 1000 points are easy made
	valid = 1000

	# The large room has extra slot, usage costs 50 points:
	escapeRoom = 0
	for key in timetable:
		if key[1] == 4:
			escapeRoom -= 50

	# One point is detracted for every student that doesn't fit in the room
	capacityOverload = 0
	for activity in activities:
		if classrooms[activity.slot[2]].capacity < len(activity.students):
			capacityOverload += (classrooms[activity.slot[2]].capacity - len(activity.students))

	# One point is detracted for every moment (the first two values of the tuple-slot) that a students has 2 activities
	studentConflict = 0
	for student in students:
		slots = []
		for activity in student.activities:
			slots.append(activity.slot[0:2])
		studentConflict -= (len(slots) - len(set(slots)))

	# a subject that is spread evenly over the week is worth 20 points. However, some subjects have multiple groups 
	# for worklectures and practica. For those I calculate for all the groups whether they qualify for 20 points. The 
	# aggregated score is then divided by the number of groups to ensure a subject cannot score more than 20 points

	subjectEvenlySpread = 0
	overlapScore = 0
	for subject in subjects:
		lectures, workLectures, practicas = [], [], []
		for activity in subject.activities:
			if activity.kind == "WorkLecture":
				workLectures.append(activity.slot[0])
			if activity.kind == "Practicum":
				practicas.append(activity.slot[0])			
			if activity.kind == "Lecture":
				lectures.append(activity.slot[0])

		i, j = 0, 0 

		if workLectures and practicas:
			num = len(workLectures) * len(practicas)
			for wl in workLectures:
				for pr in practicas:
					[i,j] = getSpreadOverlapScore(i,j, lectures + [wl] + [pr])

		elif workLectures or practicas:
			num = len(workLectures) + len(practicas)
			for act in workLectures + practicas:
				[i,j] = getSpreadOverlapScore(i,j, lectures + [act])

		else:
			num = 1
			[i,j] = getSpreadOverlapScore(i,j, lectures)

		overlapScore -= Decimal(str(i / num)).quantize(Decimal('.01'))
		subjectEvenlySpread += Decimal(str(j / num)).quantize(Decimal('.01'))

	# final score
	studentScore = capacityOverload + studentConflict
	subjectScore = overlapScore + subjectEvenlySpread
	score = valid + escapeRoom + studentScore + subjectScore
	#print(score, escapeRoom, capacityOverload, studentConflict, overlapScore, subjectEvenlySpread)
	#print(score)
	return score

def getSpreadOverlapScore(i, j, combiActivities):
	overlapScore = (len(combiActivities) - len(set(combiActivities))) * 10
	spreadScore = 0

	# if there is overlap no ideal spread is possible
	if overlapScore == 0:
		combiActivities.sort()

		if len(combiActivities) == 2:	
			if combiActivities == [0,3] or combiActivities == [1,4]:
				spreadScore = 20
			else:
				spreadScore = 0
		elif len(combiActivities) == 3:
			if combiActivities == [0,2,4]:
				spreadScore = 20
			else:
				spreadScore = 0
		elif len(combiActivities) == 4:
			if combiActivities == [0,1,3,4]:
				spreadScore = 20
			else:
				spreadScore = 0
		elif len(combiActivities) == 5:
			if combiActivities == [0,1,2,3,4]:
				spreadScore = 20
			else:
				spreadScore = 0

	i += overlapScore
	j += spreadScore

	return [i , j]