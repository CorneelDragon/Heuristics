# Heuristics
Code for 'programmeertheorie' course of the minor programming on the UvA. I developed three algorithms in order to found solutions for an instance of the univeristy timetable program (for a description of instance, see: heuristieken.nl/wiki/index.php?title=Lectures_%26_Lesroosters).

#### Paper
See my paper for the whole shebang

#### Data

The bare data is in the following csv's:  
[studens and their courses](studenten_roostering.csv)  
[courses](vakken.csv)  
[rooms](zalen.csv)  

Additional information regarding this data is saved in the following excel files:  
[cleaned students file](studenten_clean.csv)  
[students file with courses split](studenten_exploration.xls)  
[courses with additional calculations](vakken_calculations.xlsx)  

#### Representation 
The following code translates the given data and information to python code  
[import data from csv](csvFilesController.py)  
[classes](classes.py)  
[scorefunction implementation](scoreFunction.py)  

#### Heuristics and local search techniques  
[Hillclimber](hillclimber.py)  
[Simulated Annealing](simulatedAnnealing.py)  
[Genetic Algorithm](genetics.py)
* [crossover methods](reproduction.py)  

[Student Optimalization](studentOptimalization.py)  
[Room Optimalization](roomOptimalization.py)  

[Manager to create 70 roster with each algorithm](taskManager.py)  

#### Visualization  
[translate folder of rosters to json](visual.py)  
[json with necessary data for visual](visuals/visual.json)  
[javascript to dynamically show data](visuals/roster.js)  
[html with per visualized roster timetables per room / subject / student + one menu for all suboptimal socres](visuals/rosters.html)  
[css to make it pretty](visuals/rosters.css)  

#### Analysis of scores
[Examples of score development per algorithm](exports.xlsx)  
[Exporting scores of computer 1 to Excel](scoresGraph_computer_1.py)  
[Same for computer 2](scoresGraph_computer_2.py)  
[Scores of computer 1](scoresGraph_computer1.xls)  
[Scores of computer 2](scoresGraph_computer_1.xls)  

#### Analysis of rosters
[classes for roster importation](classesImport.py)  
[Importing roster and trying to improve them further](importForImprovement.py)  
[Script for analyzing the used the slots per day](ImportTestDays.py)  
[Exporting per type of activity on which day it falls for all good rosters](importForComparison.py)  
[Comparison per type of activity for good and really rosters](activitySpread.xls)  
[Attempt to compare the rosters with each other](importCompareRosters.py)  

