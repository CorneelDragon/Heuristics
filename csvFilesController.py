"""

Author: Corneel den Hartogh
Course: Heuristics

Description: Transform data from csv to python

"""

import csv

students = []

with open('studenten_clean.csv', 'r') as csvfile:
    r = csv.reader(csvfile, delimiter=',', quotechar='|')

    # Skip title
    next(r, None)

    for row in r:
        students.append(row)

subjects = []

with open('vakken.csv', 'r') as csvfile:
    r = csv.reader(csvfile, delimiter=',', quotechar='|')

    # Skip title
    next(r, None)

    for row in r:
        subjects.append(row)

classrooms = []

with open('zalen.csv', 'r') as csvfile:
    r = csv.reader(csvfile, delimiter=',', quotechar='|')

    # Skip title
    next(r, None)

    for row in r:
        classrooms.append(row)
