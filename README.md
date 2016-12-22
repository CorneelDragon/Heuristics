# Heuristics
Code for 'programmeertheorie' course of the minor programming on the UvA. I developed three algorithms in order to found solutions for an instance of the univeristy timetable program (for a description of instance, click [here](http://www.heuristieken.nl/wiki/index.php?title=Lectures_%26_Lesroosters)).

The Simulated Annealing (with local search techniques) algorithm deliverd continuously rosters with scores above 99% of the optimal score and the best result was 99.64% of the best score (1411, with possible scores between the -6541 and 1440). While I did not prove this roster was the best roster possible it is without doubt a very strong result). 

#### Paper
[See my paper for the whole shebang](docs/Paper.pdf)

#### Presentation (in Dutch)
It's a prezi, click [here](http://prezi.com/noxxqhy06dsf/) to see it,.

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
The following code translates the given data and information to python code:  
[import data from csv](csvFilesController.py)  
[classes](classes.py)  
[scorefunction implementation](scoreFunction.py)  

#### Heuristics and local search techniques  
I developed three the following algorithms and local search for student- and room optimalization:  
[Hillclimber](hillclimber.py)  
[Simulated Annealing](simulatedAnnealing.py)  
[Genetic Algorithm](genetics.py) (including: [crossover methods](reproduction.py))  

[Student Optimalization](studentOptimalization.py)  
[Room Optimalization](roomOptimalization.py)  

[Manager to create 70 roster with each algorithm](taskManager.py)  

#### Produced Rosters
I generated rosters on two computers. In addition, I have some old rosters from preliminary tests and I optimized the best rosters (with scores above 99.5%):
[first made rosters](old rosters)
[rosters computer 1](rosters_computer_1)
[rosters computer 2](rosters_computer_2)
[selected best performing rosters](top_rosters)
[the best performing rosters optimized](imported_rosters)

#### Visualization  
I made a visual with an export to json:  
[translate folder of rosters to json](visual.py)  
[json with necessary data for visual](visuals/visual.json)  
[javascript to dynamically show data](visuals/roster.js)  
[html with per visualized roster timetables per room / subject / student + one menu for all suboptimal socres](visuals/rosters.html)  
[css to make it pretty](visuals/rosters.css)  

#### Analysis of scores
I did on two computers 70 runs and exported the scores to excel (and visualized them there):  
[Examples of score development per algorithm](exports.xlsx)  
[Exporting scores of computer 1 to Excel](scoresGraph_computer_1.py)  
[Same for computer 2](scoresGraph_computer_2.py)  
[Scores on computer 1](scoresGraph_computer1.xls)  
[Scores on computer 2](scoresGraph_computer_1.xls)  

#### Analysis of rosters
Finally, I wanted to analyze the rosters themselves. This is how far I got:  
[classes for roster importation](classesImport.py)  
[Importing roster and trying to improve them further](importForImprovement.py)  
[Script for analyzing the used the slots per day](ImportTestDays.py)  
[Exporting per type of activity on which day it falls for all good rosters](importForComparison.py)  
[Comparison per type of activity for good and really rosters](activitySpread.xls)  
[Attempt to compare the rosters with each other](importCompareRosters.py)
[Script that provides number of occurences per conflict in the 20 optimized rosters](exportIssues.py)

