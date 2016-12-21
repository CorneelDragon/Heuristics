"""
All the classes for this endeavor:

- Classroom
- Subject
 - Activity
- Student 

"""
import datetime
import copy
import math
import random
import sys
import json
sys.setrecursionlimit(10000)

class Classroom:
    def __init__(self, room_number, capacity):
        self.room_number = room_number
        self.capacity = int(capacity)

        self.slots = []
    
    def __str__(self):
        return self.room_number


class Subject:
    def __init__(self, name, n_lectures, n_workLectures, w_maxStud, 
                 n_practicas, p_maxStud):
        
        self.name = name
        self.students = []
        self.activities = []

        """
        self.activities = [Activity(self, "Lecture", i, "nvt") for i in range(int(n_lectures))] + \
                        [Activity(self, "WorkLecture", i, w_maxStud) for i in range(int(n_workLectures))] + \
                        [Activity(self, "Practicum", i, p_maxStud) for i in range(int(n_practicas))]
        """

    def __str__(self):
        return self.name

    """
    def setActivities(self):
        newActivities = []
        for activity in self.activities:
            if activity.maxStud:
                # Calculate number of groups and the number of students per lecture then round up
                nGroups = math.ceil(len(self.students) / activity.maxStud)
                subjectStud = len(self.students)
                activityStudents = copy.copy(self.students)

                # For every activity, create a group and add students
                for number in range(nGroups):
                    activity = copy.copy(activity)
                    activity.group = number
                    activity.amountStud = round(subjectStud / (nGroups - number))
                    subjectStud -= activity.amountStud  
                    activity.students = activityStudents[0:activity.amountStud]
                    del activityStudents[0:activity.amountStud]
                    activity.assignActivitiesToStudents()
                    newActivities.append(activity)

            # when maxStud is zero
            else:
                activity.students = self.students
                activity.assignActivitiesToStudents()
                activity.amountStud = len(activity.students)
                newActivities.append(activity)

        self.activities = newActivities
    """

# While connected to subjects (who set them) activities have their own class
class Activity:
    def __init__(self, subject, kind, lecture_number, group, slot, maxStud, students):
        self.subject = subject
        self.kind = kind
        
        self.lecture_number = lecture_number

        if maxStud == "nvt":
            self.maxStud = 0
        else:
            self.maxStud = int(maxStud)
        
        self.students = students

        self.group = group
        self.amountStud = len(self.students)
        self.slot = tuple(slot)

        self.assignActivitiesToStudents()
        
    def __str__(self):
        return "Subject: %s Kind: %s Lecture number: %s Group: %s amountStud: %d " % (self.subject.name, self.kind, self.lecture_number, self.group, self.amountStud)

    def assignActivitiesToSubject(self, roster):
        for subject in roster.subjects:
            if self.subject.name == subject.name:
                subject.activities.append(self)

    def assignActivitiesToStudents(self):
        for student in self.students:
            student.activities.append(self)

    def __eq__(self, other):
        if other is None:
            return False
        return (self.subject.name, self.kind, self.lecture_number, self.group) == (other.subject.name, other.kind, other.lecture_number, other.group)

# A student object has name and id values, plus a list of subject-objects
class Student:
    def __init__(self, surname, name, studentId, subject1, subject2, 
                 subject3, subject4, subject5, subject_dct):
        
        self.surname = surname
        self.name = name
        self.studentId = studentId
        
        self.subjects = []
        self.__addSubject(subject1, subject_dct)
        self.__addSubject(subject2, subject_dct)
        self.__addSubject(subject3, subject_dct)
        self.__addSubject(subject4, subject_dct)
        self.__addSubject(subject5, subject_dct)

        self.__addStudentToSubject()      
        
        self.activities =[]

    def __str__(self):
        return "%s" % (self.studentId)
    
    def __addSubject(self, subject, subject_dct):
        if subject != "":
            self.subjects.append(subject_dct[subject])
    
    def __addStudentToSubject(self):
        for subject in self.subjects:
            subject.students.append(self)

class Roster:
    def __init__(self,classrooms, subjects, students):

        self.classrooms = [Classroom(x[0], x[1]) for x in classrooms]

        self.subjects = [Subject(x[0], x[1], x[2], x[3], x[4], x[5]) for x in subjects]
        subject_dct = {x.__str__(): x for x in self.subjects}

        self.students = [Student(x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7], subject_dct) 
                    for x in students]

        self.studentsActiveFirst = sorted(self.students, key=lambda x:len(x.subjects), reverse=True)

        self.activities = []





        """

        for x in self.subjects:
            x.setActivities()

        self.activities = []
        for x in self.subjects:
            for y in x.activities:
                if y.kind == "Lecture":
                    self.activities.append(y)
        for x in self.subjects:
            for y in x.activities: 
                if y.kind == "WorkLecture":
                    self.activities.append(y)
        for x in self.subjects:
            for y in x.activities: 
                if y.kind == "Practicum":
                    self.activities.append(y)
        """
    def fillInRoster(self):
        self.timetable = {}

        # set the timetable
        for activity in self.activities:
            # set activity in the roster slot
            self.timetable[activity.slot] = activity

    def getSlot(self):
        # 7 rooms, 5 days, 4 timeslots for almost all rooms
        room = random.randint(0,len(self.classrooms)-1)
        day = random.randint(0,4)
        time = 0

        # the large room has an extra slot
        if room == 5:
            time = random.randint(0,4)
        else:
            time = random.randint(0,3)
        self.slot = (day,time,room)

    def exportRoster(self, method, score,runtime):

        score = str(score)
        runtime = str(round(runtime, 2))
        time = datetime.datetime.now().strftime("%m.%d_%H.%M")
        name = method+'_'+score+'_'+runtime+'_'+time

        issues = self.setIssues()


        export = {"name": name, "roster" : {"activities":[{"activity": {"slot" : activity.slot, "subject" : activity.subject.name, "kind" : activity.kind, 
        "lecture_number" : activity.lecture_number, "group" : activity.group, "amountStud": len(activity.students), "maxStud" : activity.maxStud, 
        "students": [student.name + " " + student.surname + " " + student.studentId for student in activity.students] } } for activity in self.activities],
        
        "students":[{"student" : student.name + " " + student.surname + " " + student.studentId } for student in self.students],

        "classrooms": [{"number" : room.room_number, "capacity" : room.capacity } for room in self.classrooms],
    
        "subjects": [{"subject" : subject.name } for subject in self.subjects],
        "issues" : [{"category": issue[0], "reference" : issue[1] } for issue in issues]}}

        # [{ "subject" : activity.subject.name, "kind" : activity.kind, "lecture_number" : activity.lecture_number, "group" : activity.group]}
        jsonString = json.dumps(export, indent=4)

        f = open('imported_rosters/'+name+'.json', 'w')
        print(jsonString, end="", file=f)
        f.close()

    # For visualization issues need to be identified
    def setIssues(self):
        issues = []

        for index,room in enumerate(self.classrooms):
            for activity in self.activities:
                if activity.slot[2] == index:
                    if len(activity.students) > room.capacity or activity.slot[1] == 4:
                        issues.append(["Room", room.room_number])
                        break
                    else:
                        continue
                    break

        for subject in self.subjects:
            subjectDays = []
            uniqueActivities = 0
            for index, activityOne in enumerate(subject.activities):
                subjectDays.append(activityOne.slot[0])
                if activityOne.kind == "Lecture" or activityOne.group == 0:
                    uniqueActivities += 1
                if index < len(subject.activities):
                    for activityTwo in subject.activities[index+1:]:
                        if activityOne.slot[0] == activityTwo.slot[0] and (activityOne.kind != activityTwo.kind or activityOne.kind == "Lecture"):
                            issues.append(["Subject", subject.name])
                            break
                    else:
                        continue
                    break

            if not issues or subject.name != issues[-1][1]:
                if uniqueActivities == 2:
                    problem = False
                    for day in subjectDays:
                        if day != 0 and day != 3:
                            problem = True 
                            break
                    if problem == True:
                        problem = False
                        for day in subjectDays:
                            if day != 1 and day != 4:
                                issues.append(["Subject", subject.name])
                                break
                elif uniqueActivities == 3:
                    for day in subjectDays:
                        if day == 1 or day == 3:
                            issues.append(["Subject", subject.name])
                            break
                elif uniqueActivities == 4:
                    for day in subjectDays:
                        if day == 2:
                            issues.append(["Subject", subject.name])
                            break

        for student in self.students:
            slotList = []
            for activity in student.activities:
                slotList.append(activity.slot[0:2])
            if len(slotList) > len(set(slotList)):
                studentIssue = student.name + " " + student.surname + " " + student.studentId
                issues.append(["Stud.", studentIssue])

        return issues

    # this module is faster than douplicating the roster with deep.copy   
    def duplicateRoster(newRoster, bestRoster):
        newRoster.timetable = {}
        for x in range(5):
            for y in range(5):
                for z in range(len(newRoster.classrooms)):
                    if(x,y,z) in bestRoster.timetable:
                        for activity in newRoster.activities:
                            if bestRoster.timetable[(x,y,z)] == activity:
                                newRoster.timetable[(x,y,z)] = activity
                                activity.slot = (x,y,z)
        return newRoster
