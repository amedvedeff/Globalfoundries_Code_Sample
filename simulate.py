from simulation import Simulation
import sys

direcotOrGUI = sys.argv[1]
solutionID = sys.argv[2]
simulation = Simulation(direcotOrGUI, solutionID)
simulation.run()
simulation.get_fitness(solutionID)
