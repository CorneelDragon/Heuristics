def roomOptimization(roster):
    timetable = roster.timetable
    classrooms = sorted(roster.classrooms, key=lambda x:x.capacity, reverse=True)

    for x in range(5):
        for y in range(5):
            activityList = []
            for z in range(len(classrooms)):
                if (x,y,z) in timetable:
                    activityList.append(timetable[(x,y,z)])

            activityList = sorted(activityList, key=lambda x:len(x.students), reverse=True)

            """
            if genetics = True:
                while len(classrooms) - len(activityList) > 0:
                    activityList.insert(randrange(len(activityList)+1), None)
            """            
            while len(activityList) < 7:
                activityList.append(None)

            for i, activity in enumerate(activityList):
                for j, room in enumerate(roster.classrooms):
                    if classrooms[i] == room:
                        if activity != None:
                            activity.slot = (x,y,j)
                            timetable[(x,y,j)] = activity
                        else:
                            if (x,y,j) in timetable:
                                del timetable[(x,y,j)]

    roster.timetable = timetable

    return roster