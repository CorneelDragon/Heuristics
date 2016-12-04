import random
import copy
import time
from decimal import Decimal

from csvFilesController import classrooms,subjects,students
from classes import Classroom,Subject,Activity,Student,Roster
from scoreFunction import ScoreFunction
from studentOptimization import studentOptimization

start_time = time.time()

bestRoster = Roster(classrooms,subjects, students)
bestRoster.fillInRoster()

bestScoreClass = ScoreFunction(bestRoster)
bestScore = bestScoreClass.getScore()

scores = []
scores.append(bestScore)

i = 0

# after a cycle of length 'period' we check if there was still progress
while len(scores) == 1 or scores[-1] > 5 + scores[-2]:

    t = 0
    period = 1

    while t < period:

        newRoster = copy.deepcopy(bestRoster)

        newRoster.getSlot()
        slotOne = newRoster.slot
        newRoster.getSlot() 
        slotTwo = newRoster.slot

        if slotOne in newRoster.timetable:
            activityOne = newRoster.timetable[slotOne]

        else:
            activityOne = None

        if slotTwo in newRoster.timetable:
            activityTwo = newRoster.timetable[slotTwo]
        else:
            activityTwo = None

        if activityOne is not None:
            newRoster.timetable[slotTwo] = activityOne
            activityOne.slot = slotTwo

        else:
            if activityTwo is not None:
               del newRoster.timetable[slotTwo]         

        if activityTwo is not None:
            newRoster.timetable[slotOne] = activityTwo
            activityTwo.slot = slotOne

        else:
            if activityOne is not None:
                del newRoster.timetable[slotOne]

        # make sure students are sorted appropriately over the WorkLectures and Practica
        # get the timeslots (first 2 values of slot) of the activities and keep only the one's that are double rostered
        newRoster = studentOptimization(newRoster)

        scoreClass = ScoreFunction(newRoster)
        score = scoreClass.getScore()

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