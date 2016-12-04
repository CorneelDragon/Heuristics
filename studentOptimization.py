import copy

def studentOptimization(roster):
    for student in roster.studentsActiveFirst:
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
            for activity in roster.activities:            
                if activity.kind == altActivity.kind and activity.subject == altActivity.subject and  \
                activity.slot[0:2] not in timeslotsDouble and activity.group is not altActivity.group:
                    # if other group is not full, put the student there
                    if activity.maxStud > len(activity.students):
                        changeStudent(student,activity, altActivity)
                        activity.amountStud += 1
                        altActivity.amountStud -= 1
                        break

                    elif activity.maxStud == activity.amountStud:
                        # if other group is full, but in it are students that are unlikely to have conflicts (since they have only subject) switch
                        # first check students with less subjects
                        activity.studentsReversed = sorted(activity.students, key=lambda x:len(x.subjects))
                        suboptimalStudent = None
                        for studentSwitch in activity.studentsReversed:
                            if len(studentSwitch.subjects) == 1:
                                changeStudent(student,activity, altActivity)
                                switchStudent(studentSwitch,activity, altActivity)
                                break

                            elif len(studentSwitch.subjects) > 1:
                                # try other students (but not the ones with more subjects, since they are altready optimalized
                                timeslotsSwitch = []
                                for activ in studentSwitch.activities:
                                    timeslotsSwitch.append(activ.slot[0:2])

                                for timeslot in timeslotsSwitch:
                                    if altActivity.slot[0:2] == timeslot:
                                        # when we have a student with less subjects but still conflicting schedules, we remember the student
                                        #if activity == roster.activities[len(roster.activities)-1] and \
                                        if len(studentSwitch.subjects) <= len(student.subjects) and suboptimalStudent == None:
                                            suboptimalStudent = studentSwitch
                                        break
                                else:
                                    changeStudent(student,activity, altActivity)
                                    switchStudent(studentSwitch,activity, altActivity)
                                    suboptimalStudent = None
                                    break
                                continue
                            else:
                                continue
                        # switch students, maybe we are able to optimalize the other student's roster better
                        if suboptimalStudent != None:
                            changeStudent(student,activity, altActivity)
                            switchStudent(suboptimalStudent,activity, altActivity)                         
                        break
                    else:
                        continue
                    break
                else:
                    continue
                break
    return roster

def changeStudent(student, activity, altActivity):
    student.activities.remove(altActivity)
    altActivity.students.remove(student)
    student.activities.append(activity)
    activity.students.append(student)

def switchStudent(studentSwitch, activity, altActivity):
    studentSwitch.activities.remove(activity)
    activity.students.remove(studentSwitch)
    studentSwitch.activities.append(altActivity)
    altActivity.students.append(studentSwitch)