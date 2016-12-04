import random
import copy
import time
from decimal import Decimal

from csvFilesController import classrooms,subjects,students
from classes import Classroom,Subject,Activity,Student,Roster
from scoreFunction import getScore
from studentOptimization import studentOptimization
from roomOptimization import roomOptimization

start_time = time.time()

bestRoster = Roster(classrooms,subjects, students)
bestRoster.fillInRoster()

bestScore = getScore(bestRoster)

scores = []
scores.append(bestScore)

i = 0

# after a cycle of length 'period' we check if there was still progress
while len(scores) == 1 or scores[-1] > scores[-2]:

    t = 0
    period = 1000

    while t < period:

        newRoster = copy.deepcopy(bestRoster)

        newRoster.getSlot()
        slotOne = newRoster.slot
        newRoster.getSlot() 
        slotTwo = newRoster.slot

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
        #test = score - oldScore
        #print("test: ", test)
        if score > bestScore:
            bestRoster = newRoster
            bestScore = score
            tBest = (i * period) + t

        print(bestScore)
        t += 1

    scores.append(bestScore)
    i += 1

print(bestScore, tBest,(i*period)+t)
bestRoster.exportRoster("hillclimber",bestScore)
print("--- %s seconds ---" % (time.time() - start_time))