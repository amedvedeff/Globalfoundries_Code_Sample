import copy
from solution import Solution
import constants as c
import os
import random

class AFPO:
    """
    A class used to implement the Age-Fitness Pareto Optimization
    algorithm as described here:https://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.375.6168&rep=rep1&type=pdf
    ...

    Attributes
    __________
    NextAvailableID : int
        Assigns an ID to each Solution generated

    Population : Solution array
        Holds all of the Solutions created or maintained in each generation

    Methods
    ________
    expand_population_for_one_generation()
        Increase population by adding random individuals to the population

    contract_population_for_one_generation()
        Decreases population size by comparing the fitness and age of two random individuals in a population
        and deleting the older, less fit indiviuals until the original population size is acquired

    evolve()
        Expands the population, then determines fitness values for each individual, followed by a contraction of
        population and subsequent incrementing of each individual's age

    spawn()
        Creates the initial set of individuals in the population and assigns each an ID

    mutate()
        Calls the mutate method from Solution for each individual in the population

    show_best()
        Selects the fittest individual and displays the robot in motion in the PyBullet GUI

    evaluate(Solutions)
        Determines the fitness value for each individual by simulating their behavior in PyBullet

    is_younger(Solution1, Solution2)
        Compares the MyAge value for Solution1 and Solution2, returns True if Solution1.MyAge is less, False otherwise

    is_fitter(Solution1, Solution2)
        Compares the Fitness value for Solution1 and Solution2, returns True if Solution1.Fitness is less than or equal
        to Solution2.Fitness, False otherwise.

    increment_age_of_population()
        All individuals in population have MyAge value increased by 1

    add_random_individuals_to_population()
        Doubles the size of the population by adding more random individuals

    population_reorder(randNum)
        Assigns new position for an individual after the population size has decreased

    show_population()
        Prints all members of the population and their associated fitness value to terminal
    """
    def __init__(self):
        self.NextAvailableID = 0
        self.Population = {}
        for x in range(c.POPULATION_SIZE):
            self.Population[x] = Solution(self.NextAvailableID)
            self.NextAvailableID += 1

        #These commands clear any files that were not properly deleted in the last run
        os.system("rm brain*.nndf")
        os.system("rm fitness*.txt")
        os.system("rm tmp*.txt")

    def expand_population_for_one_generation(self):
        self.spawn()
        self.mutate()
        self.add_random_individuals_to_population()

    def contract_population_for_one_generation(self):
        """
        This method compares two individuals at random in the population.
        If one individual is both younger and fitter than the other, then the second older and less fit
        individual is removed from the population.

        Parameters:
        none

        Returns:
        none

       """
        while len(self.Population) != c.POPULATION_SIZE:
            RandNum1 = random.randint(0, (len(self.Population) - 3))
            RandNum2 = random.randint(0, (len(self.Population) - 3))

            if (self.is_younger(RandNum1, RandNum2) and self.is_fitter(RandNum1, RandNum2)):
                del self.Population[RandNum2]
                self.population_reorder(RandNum2)

            if (self.is_younger(RandNum2, RandNum1) and self.is_fitter(RandNum2, RandNum1)):
                del self.Population[RandNum1]
                self.population_reorder(RandNum1)

    def evolve(self):
        for currentGeneration in range(c.NUM_GENERATIONS):
            self.expand_population_for_one_generation()
            self.evaluate(self.Population)
            self.contract_population_for_one_generation()
            self.increment_age_of_population()


    def spawn(self):
        for x in range(c.POPULATION_SIZE):
            self.Population[c.POPULATION_SIZE + x] = copy.deepcopy(self.Population[x])
            self.Population[c.POPULATION_SIZE + x].MyID = self.NextAvailableID
            self.NextAvailableID += 1

    def mutate(self):
        for x in range(c.POPULATION_SIZE):
            self.Population[c.POPULATION_SIZE + x].mutate()

    def show_best(self):
        best = 0
        for x in range(c.POPULATION_SIZE):
            if self.Population[best].Fitness > self.Population[x].Fitness:
                best = x

        self.Population[best].start_simulation("GUI")

    def evaluate(self, Solutions):
        for x in range(len(self.Population)):
            Solutions[x].start_simulation("DIRECT")

        for x in range(len(self.Population)):
            Solutions[x].wait_for_simulation_to_end()

    def is_younger(self, Solution1, Solution2):
        if self.Population[Solution1].MyAge > self.Population[Solution2].MyAge:
            return False
        if self.Population[Solution1].MyAge <= self.Population[Solution2].MyAge:
            return True

    def is_fitter(self, Solution1, Solution2):
        if self.Population[Solution1].Fitness >= self.Population[Solution2].Fitness:
            return False
        if self.Population[Solution1].Fitness < self.Population[Solution2].Fitness:
            return True

    def increment_age_of_population(self):
        for x in range(len(self.Population)):
            self.Population[x].MyAge += 1

    def add_random_individuals_to_population(self):
        for x in range(c.NUM_INDIVIDUALS_ADDED_PER_GENERATION):
            self.Population[(2 * c.POPULATION_SIZE) + x] = Solution(self.NextAvailableID)
            self.NextAvailableID += 1

    def population_reorder(self, randNum):
        if randNum == len(self.Population):
            randNum = randNum
        else:
            while randNum < len(self.Population) - 1:
                self.Population[randNum] = self.Population[randNum + 1]
                randNum += 1
            del self.Population[randNum]

    def show_population(self):
        for x in range(len(self.Population)):
            print("The fitness of the element at " + str(x) + " is " + str(
                self.Population[x].Fitness) + ". There are " + str(len(self.Population)) + "remaining.")
