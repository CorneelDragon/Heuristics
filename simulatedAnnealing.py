import random
import copy
import time
import math
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
allTimeBestScore = bestScore

temp = 100
i = 0


scores = []
scores.append(bestScore)

while i < 20 or i < 5 + iHighscore:

    t = 0
    period = 1000

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

        delta = score - bestScore

        if delta > 0:
            bestRoster = newRoster
            bestScore = score
            iBest = (i*period)+ t
            #print(bestScore, tBest)


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

        temp = 100 * math.pow(10 / 100,((i*period)+t)/20000)
        t += 1
        print(bestScore)

    scores.append(allTimeBestScore)
    i +=1

print(bestScore, iBest, (i*period)+ t)
print(allTimeBestScore, allTImeBestI)
bestRoster.exportRoster("annealing",bestScore)
allTimeBestRoster.exportRoster("annealing",allTimeBestScore)
print("--- %s seconds ---" % (time.time() - start_time))