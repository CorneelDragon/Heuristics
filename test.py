from hillclimber import hillclimber
from simulatedAanneling import simulatedAanneling
i = 200
while (i < 1000):
	if i % 3 == 0:
		simulatedAanneling()
	else:
		hillclimber()

	i += 1