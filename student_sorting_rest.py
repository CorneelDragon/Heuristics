


            """
            Random students

            # in addition to rosterinfg of activities students can be rostered across groups as well
            # shuffle the students in subjects that multiple groups
            if activity.kind != "Lecture" and activity.group == 0:
                random.shuffle(activity.subject.students)
                activity.subject.studentsRandom = copy.copy(activity.subject.students)

            # get students into the activity if it is empty
            if not activity.students:
                activity.students = activity.subject.studentsRandom[0:activity.amountStud]
                activity.assignActivitiesToStudents()
                del activity.subject.studentsRandom[0:activity.amountStud]

            """




 """
    Student sorting

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
                if activity.kind == altActivity.kind and activity.subject == altActivity.subject and activity.slot not in timeslotsDouble:
                    # if other group is not full, put the student there
                    if activity.maxStud > activity.amountStud:
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
                                for activity in studentSwitch.activities:
                                    timeslotsSwitch.append(activity.slot[0:2])

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
                                break
                            else:
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
            else:
                continue
            break
        """

                