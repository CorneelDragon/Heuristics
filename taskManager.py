from hillclimber import hillclimber
from simulatedAnnealing import simulatedAnnealing
from genetics import genetics

i = 0
while i < 70:
	hillclimber()
	simulatedAnnealing()
	genetics()
	i += 1