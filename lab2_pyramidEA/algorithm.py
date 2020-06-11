import numpy
import statistics
import matplotlib.pyplot as plt
from random import randint

from individual import Individual
from population import Population


class Algorithm:

    def __init__(self, problem, paramfile):
        self.__problem = problem
        self.load(paramfile)

    def load(self, paramfile):
        file = open(paramfile, "r")
        self.__probability = float(file.readline().strip())
        self.__population_size = int(file.readline().strip())
        self.__generations_number = int(file.readline().strip())
        file.close()

        print("mutation probability: " + str(self.__probability))
        print("population size: " + str(self.__population_size))
        print("nr of iterations: " + str(self.__generations_number) + "\n")


    def iteration(self):
        """
        pop: the current population
        pM: the probability the mutation to occure
        cubes: dict, mapping keys to cube sizes and colors
        """
        i1 = randint(0, self.__population_size - 1)
        i2 = randint(0, self.__population_size - 1)
        if i1 != i2:
            ind1 = self.__population.get_list()[i1]
            ind2 = self.__population.get_list()[i2]
            c = Individual.crossover1(ind1, ind2, self.__problem.get_cubes())
            c.mutate(self.__probability, self.__problem.get_cubes())

            f1 = ind1.get_fitness()
            f2 = ind2.get_fitness()
            fc = c.get_fitness()
            if (f1 > f2) and (f1 > fc):
                self.__population.get_list()[i2] = c
            if (f2 > f1) and (f2 > fc):
                self.__population.get_list()[i1] = c

        fitnesses = [x.get_fitness() for x in self.__population.get_list()]
        self.__fitnessvar.append(statistics.mean(fitnesses))


    def run(self):
        self.__fitnessvar = []

        self.__population = Population(self.__population_size,self.__problem.get_cubes())
        for i in range(self.__generations_number):
            self.iteration()

        plt.plot(self.__fitnessvar)
        plt.ylabel('fitness means')
        plt.xlabel('iterations')
        plt.show()

        return self.__population.evaluate()


    def statistics(self):
        fitnesses = []
        individuals = []

        for i in range(10):
            res = self.run()
            print("#" + str(i+1) + ": fitness: " + str(res.get_fitness()) + ", individual: " + str(res.get_fenotype(self.__problem.get_cubes())))

            fitnesses.append(int(res.get_fitness()))
            individuals.append(res.get_genotype())

        print("\nmean of fitnesses:  \t" + str(statistics.mean(fitnesses)))
        print("stdev of fitnesses: \t" + str(statistics.stdev(fitnesses)))

 

        #print("\nmean of genotypes: ")
        #print(*map(statistics.mean, zip(*individuals)))
        #print("\nstdev of genotypes: ")
        #print(*map(statistics.stdev, zip(*individuals)))
