import random
import copy
import time
import math
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
allTimeBestScore = bestScore

i = 0

scores = []
scores.append(bestScore)

temp = 200

while i < 20 or i < 2 + iHighscore:

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
        newRoster = roomOptimization(newRoster)
        score = getScore(newRoster)

        delta = score - bestScore

        if delta > 0:
            bestRoster = newRoster
            bestScore = score
            iBest = (i*period)+ t

            if score > allTimeBestScore:
                allTimeBestScore = score
                allTimeBestRoster = newRoster
                allTImeBestI = (i*period)+t
                iHighscore = i

        else: 
            p = math.exp(delta / Decimal(temp))
            if random.random() < p :

                bestRoster = newRoster
                bestScore = score
                iBest = (i*period)+ t
                #print(bestScore, tBest)

        temp = 200 * math.pow(10 / 200,((i*period)+t)/20000)
        t += 1
        print(bestScore)

    scores.append(allTimeBestScore)
    i +=1

print(bestScore, iBest, (i*period)+ t)
print(allTimeBestScore, allTImeBestI)
bestRoster.exportRoster("annealing",bestScore)
allTimeBestRoster.exportRoster("annealing",allTimeBestScore)
print("--- %s seconds ---" % (time.time() - start_time))