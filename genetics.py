from operator import itemgetter
import copy
import random
import time

from csvFilesController import classrooms,subjects,students
from classes import Classroom,Subject,Activity,Student,Roster
from scoreFunction import ScoreFunction
from studentOptimization import studentOptimization

start_time = time.time()

rosterPopulation = []

# get a random population of 20
while len(rosterPopulation) < 20:
    newRoster = Roster(classrooms,subjects, students)
    newRoster.fillInRoster()
    scoreClass = ScoreFunction(newRoster)
    score = scoreClass.getScore()
    rosterPopulation.append([newRoster, score])

scores = []
scores.append(rosterPopulation[19][1])
i = 0

# after a cycle of length 'period' we check if there was still progress
while len(scores) == 1 or scores[-1] > 5 + scores[-2]:

    t = 0
    period = 1000

    # number of generations
    while t < period:

        # two parents are gathered from the population of 30 and two children are made
        parents = random.sample(range(20), 2)
        childOne = Roster(classrooms,subjects, students)
        childTwo = Roster(classrooms,subjects, students)

        child = [childOne, childTwo]

        # the crossover is after the first, second or third time-slot 
        timeSlot = random.randint(1,3)

        for c in range(2):
            timetable = {}
            first = 0
            second = 0
            if c == 0:
                first = 0
                second = 1
            else:
                first = 1
                second = 0

            for x in range(5):
                for y in range(timeSlot):
                    for z in range(len(classrooms)):
                        if(x,y,z) in rosterPopulation[parents[first]][0].timetable:
                            for activity in child[c].activities:
                                if activity == rosterPopulation[parents[first]][0].timetable[(x,y,z)]:
                                    timetable[(x,y,z)] = activity
                                    activity.slot = (x,y,z)

            for x in range(5):
                for y in range(timeSlot,5):
                    for z in range(len(classrooms)):
                        if(x,y,z) in rosterPopulation[parents[second]][0].timetable and (x,y,z) not in timetable.keys() and rosterPopulation[parents[second]][0].timetable[(x,y,z)] not in timetable.values():
                            for activity in child[c].activities:
                                if activity == rosterPopulation[parents[second]][0].timetable[(x,y,z)]:
                                    timetable[(x,y,z)] = activity
                                    activity.slot = (x,y,z)

            for x in range(5):
                for y in range(timeSlot,5):
                    for z in range(len(classrooms)):
                        if(x,y,z) in rosterPopulation[parents[first]][0].timetable and (x,y,z) not in timetable.keys() and rosterPopulation[parents[first]][0].timetable[(x,y,z)] not in timetable.values():
                            for activity in child[c].activities:
                                if activity == rosterPopulation[parents[first]][0].timetable[(x,y,z)]:
                                    timetable[(x,y,z)] = activity
                                    activity.slot = (x,y,z)

            for x in range(5):
                for y in range(timeSlot):
                    for z in range(len(classrooms)):
                        if(x,y,z) in rosterPopulation[parents[second]][0].timetable and (x,y,z) not in timetable.keys() and rosterPopulation[parents[second]][0].timetable[(x,y,z)] not in timetable.values():
                              for activity in child[c].activities:
                                if activity == rosterPopulation[parents[second]][0].timetable[(x,y,z)]:
                                    timetable[(x,y,z)] = activity
                                    activity.slot = (x,y,z)

            child[c].timetable = timetable

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
                mutations = random.sample(range(129), 3)
                for mut in range(2):
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

            scoreClass = ScoreFunction(child[c])
            score = scoreClass.getScore()

            # add child to population
            rosterPopulation.append([child[c], score])

        # delete the unfittest two rosters from the populations
        rosterPopulation.sort(key=itemgetter(1))
        del rosterPopulation[0:2]

        #for roster in rosterPopulation:
            #print(roster[1])

        print(rosterPopulation[19][1])
        t += 1

    scores.append(rosterPopulation[19][1])
    i += 1

#export best roster
rosterPopulation[19][0].exportRoster("genetics",rosterPopulation[19][1])
print(rosterPopulation[19][1],(i * period) + t)

print("\n")
for roster in rosterPopulation:
    print(roster[1])

print("--- %s seconds ---" % (time.time() - start_time))