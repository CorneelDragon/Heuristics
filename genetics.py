"""

Author: Corneel den Hartogh
Course: Heuristics

Description: Genetic algorithm code

"""

from operator import itemgetter
import copy
import random
import time

from csvFilesController import classrooms,subjects,students
from classes import Classroom,Subject,Activity,Student,Roster
from scoreFunction import getScore
from studentOptimization import studentOptimization
from roomOptimization import roomOptimization
from reproduction import reproduceTimeOrDay, reproduceSubjects

def genetics():
    startTime = time.process_time()

    rosterPopulation = []

    # get a random population of 20
    while len(rosterPopulation) < 20:
        newRoster = Roster(classrooms,subjects, students)
        newRoster.fillInRoster()
        score = getScore(newRoster)
        rosterPopulation.append([newRoster, score])

    scores = []
    scores.append(rosterPopulation[19][1])
    iteration = 0

    # after a cycle of length 'period' we check if there was still progress
    while len(scores) == 1 or scores[-1] >  scores[-2]:

        t = 0
        period = 1000

        # number of generations
        while t < period:

            # two parents are gathered from the population of 30 and two children are made
            parents = random.sample(range(20), 2)
            father = rosterPopulation[parents[0]][0]
            mother = rosterPopulation[parents[1]][0]
            childOne = Roster(classrooms,subjects, students)
            childTwo = Roster(classrooms,subjects, students)

            child = [childOne, childTwo]

            for c in range(2):
                timetable = {}
                first = None
                second = None
                if c == 0:
                    first = father
                    second = mother
                else:
                    first = mother
                    second = father

                # what type of reproduction is exectued?
                case = random.randint(0,2)
                if case == 0:
                    day = random.randint(1,4)
                    timeSlot = 0
                    reproductionResult = reproduceTimeOrDay(timetable, day,timeSlot, first, second, child[c].activities, len(classrooms))

                if case == 1:
                    day = 0
                    timeSlot = random.randint(1,3)
                    reproductionResult = reproduceTimeOrDay(timetable, day,timeSlot, first, second, child[c].activities, len(classrooms))

                if case == 2:
                    reproductionResult = reproduceSubjects(timetable, first, second, child[c].activities, len(classrooms))

                child[c].timetable = reproductionResult[0]
                child[c].activities = reproductionResult[1]

                # repair if necessary, if parents are complementary ensure mutation
                mutationNeed = 0

                for activity in child[c].activities:
                    if activity.slot == ():
                        child[c].getSlot()
                        while child[c].slot in child[c].timetable:
                            child[c].getSlot()
                        child[c].timetable[child[c].slot] = activity
                        activity.slot = child[c].slot
                    else:
                        mutationNeed +=1

                if mutationNeed > 126:
                    mutations = random.sample(range(129), mutationNeed - 126)
                    for mut in range(len(mutations)):
                        activity = child[c].activities[mutations[mut]]
                        del timetable[activity.slot]
                        child[c].getSlot()
                        while child[c].slot in child[c].timetable:
                            child[c].getSlot()
                        child[c].timetable[child[c].slot] = activity
                        activity.slot = child[c].slot

                # make sure students are sorted appropriately over the WorkLectures and Practica
                # this enhancement seemed to add 50-100 to the score (which was stable over generations)
                child[c] = studentOptimization(child[c])
                child[c] = roomOptimization(child[c])

                score = getScore(child[c])

                # add child to population
                rosterPopulation.append([child[c], score])

            # delete the unfittest two rosters from the populations
            rosterPopulation.sort(key=itemgetter(1))
            del rosterPopulation[0:2]
            t += 1

        scores.append(rosterPopulation[19][1])
        iteration += 1

    # export best roster
    runtime = time.process_time() - startTime
    rosterPopulation[19][0].exportRoster("genetics",rosterPopulation[19][1],runtime)

genetics()
