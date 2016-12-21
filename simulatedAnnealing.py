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

def simulatedAnnealing():

    startTime = time.process_time()

    bestRoster = Roster(classrooms,subjects, students)
    bestRoster.fillInRoster()

    bestScore = getScore(bestRoster)
    allTimeBestScore = bestScore

    iteration = 0

    scores = []
    scores.append([bestScore,0])

    temp = 100

    # due to temperature it becomes after 30 a hillclimber (so that's where I cross the line)
    while iteration < 30 or scores[-1][0] > scores[-2][0]:

        t = 0
        period = 1000

        while t < period:

            newRoster = Roster(classrooms,subjects,students)
            newRoster = Roster.duplicateRoster(newRoster,bestRoster)

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
                iBest = (iteration*period)+ t

                if score > allTimeBestScore:
                    allTimeBestScore = score
                    allTimeBestRoster = newRoster
                    allTImeBestI = (iteration*period)+t

            else: 
                p = math.exp(delta / Decimal(temp))
                if random.random() < p :

                    bestRoster = newRoster
                    bestScore = score
                    iBest = (iteration*period)+ t

            temp = 100 * math.pow(10 / 100,((iteration*period)+t)/10000)
            t += 1
            #print(bestScore)

        scores.append([allTimeBestScore, allTImeBestI])
        iteration +=1

    runtime = time.process_time() - startTime
    #print(bestScore, iBest, ((iteration-1)*period))
    #print(allTimeBestScore, allTImeBestI)
    allTimeBestRoster.exportRoster("annealing",allTimeBestScore,runtime)
    #print("--- %s seconds ---" % (runtime))

simulatedAnnealing()