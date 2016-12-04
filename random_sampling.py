import random
import copy
import time
# import collections
#from operator import itemgetter
#from collections import OrderedDict

from csvFilesController import classrooms,subjects,students
from classes import Classroom,Subject,Activity,Student,Roster
from scoreFunction import ScoreFunction

start_time = time.time()

rosterPopulation = []

# get a random population of 20
while len(rosterPopulation) < 50000:
    newRoster = Roster(classrooms,subjects, students)
    newRoster.fillInRoster()

    # make sure students are sorted appropriately over the WorkLectures and Practica
    # get the timeslots (first 2 values of slot) of the activities and keep only the one's that are double rostered
    
    for student in newRoster.students:
        timeslots = []
        for activity in student.activities:
            timeslots.append(activity.slot[0:2])
        timeslotsDouble = copy.copy(timeslots)
        for x in set(timeslots):
            timeslots.remove(x)

        altActivities = []

        # select the activities that are double rostered and can be replaced (so only the ones that have multiple groups)
        for activity in student.activities:
            for x in set(timeslots):
                if (activity.slot[0:2] == x and activity.kind == "WorkLecture") or \
                (activity.slot[0:2] == x and activity.kind == "Practicum"):
                    altActivities.append(activity)

        for altActivity in altActivities:
            for activity in newRoster.activities:
                if activity.kind == altActivity.kind and activity.subject == altActivity.subject and \
                activity.slot[0:2] not in timeslotsDouble and activity.group is not altActivity.group:
                    # if other group is not full, put the student there
                    if activity.maxStud > len(activity.students):
                        student.activities.remove(altActivity)
                        altActivity.students.remove(student)
                        student.activities.append(activity)
                        activity.students.append(student)
                        break

                    elif activity.maxStud == activity.amountStud:
                        # if other group is full, but in it are students that are unlikely to have conflicts (since they have only subject) switch
                        for studentSwitch in activity.students:
                            if len(studentSwitch.subjects) == 1:

                                student.activities.remove(altActivity)
                                altActivity.students.remove(student)
                                student.activities.append(activity)
                                activity.students.append(student)

                                studentSwitch.activities.remove(activity)
                                activity.students.remove(studentSwitch)
                                studentSwitch.activities.append(altActivity)
                                altActivity.students.append(studentSwitch)
                                break

                            elif len(studentSwitch.subjects) < len(student.subjects):
                                # try other students (but not the ones with more subjects, since they are altready optimalized
                                timeslotsSwitch = []
                                for activ in studentSwitch.activities:
                                    timeslotsSwitch.append(activ.slot[0:2])

                                for timeslot in timeslotsSwitch:
                                    if altActivity.slot[0:2] == timeslot:
                                        break
                                else:
                                    student.activities.remove(altActivity)
                                    altActivity.students.remove(student)
                                    student.activities.append(activity)
                                    activity.students.append(student)

                                    studentSwitch.activities.remove(activity)
                                    activity.students.remove(studentSwitch)
                                    studentSwitch.activities.append(altActivity)
                                    altActivity.students.append(studentSwitch)
                                    break
                                continue
                            else:
                                continue
                            break
                        else:
                            continue
                        break
                    else:
                        continue
                    break
                else:
                    continue
                break

    scoreClass = ScoreFunction(newRoster)
    score = scoreClass.getScore()
    print(round(score, 0))
    rosterPopulation.append([newRoster, score])

print("--- %s seconds ---" % (time.time() - start_time))