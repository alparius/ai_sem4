import matplotlib.pyplot as plt
import numpy
import statistics

from ant import Ant
from problem import Problem


class Controller:

    def __init__(self, paramfile, problem):
        self.loadParams(paramfile)
        self.__problem = problem
        self.__fitnessvar = []

    def loadParams(self, paramfile):
        with open(paramfile, "r") as file:
            self.SIZE = int(file.readline().strip())
            self.NR_ITER = int(file.readline().strip())
            self.POP_SIZE = int(file.readline().strip())
            self.ALPHA = float(file.readline().strip())
            self.BETA = float(file.readline().strip())
            self.RHO = float(file.readline().strip())
            self.Q0 = float(file.readline().strip())

    def printself(self):
        print("size: " + str(self.SIZE))
        print("nr_iter: " + str(self.NR_ITER))
        print("nr_ants: " + str(self.POP_SIZE))
        print("alpha (trail importance): " + str(self.ALPHA))
        print("beta (heuristic importance): " + str(self.BETA))
        print("rho (pheromone evaporation): " + str(self.RHO))
        print("q0 (randomity constant): " + str(self.Q0))


    def iteration(self):
        # create population
        population = [Ant(self.SIZE, self.__problem.get_positions(), self.__problem.get_words(), self.__problem.get_table()) for _ in range(self.POP_SIZE)]

        # max nr of iterations is the length of the solution
        for _ in range(self.SIZE - 1):
            for ant in population:
                ant.addMove(self.__problem.get_positions(), self.__problem.get_words(), self.__trace, self.ALPHA, self.BETA, self.Q0)

        # reduce old pheromone smell a bit
        for i in range(self.SIZE * self.SIZE):
            for j in range(self.SIZE * self.SIZE):
                self.__trace[i][j] = (1 - self.RHO) * self.__trace[i][j]

        # add new pheromone smell
        dTrace = [population[i].fitness() / 3000.0 for i in range(self.POP_SIZE)]
        '''
        for i in range(self.POP_SIZE):
            for j in range(len(population[i].get_path()) - 1):
                x = population[i].get_path()[j]
                y = population[i].get_path()[j + 1]
                if y==-1 or x==-1:
                    continue
                self.__trace[x][y] = self.__trace[x][y] + dTrace[i]
        '''
        for i in range(self.POP_SIZE):
            for j in range(len(population[i].get_path())):
                if population[i].get_path()[j] == -1:
                    continue
                x = population[i].get_path()[j]
                self.__trace[x][j] = self.__trace[x][j] + dTrace[i]

        # return best ant path
        f = [[population[i].fitness(), i] for i in range(self.POP_SIZE)]
        f = max(f, key=lambda a: a[0])

        fitnesses = [x.fitness() for x in population]
        self.__fitnessvar.append(statistics.mean(fitnesses))

        #for j in range(len(population[f[1]].get_path())):
        #    x = population[f[1]].get_path()[j]
        #    self.__trace[x][j] = self.__trace[x][j] + dTrace[f[1]]*2

        print(str(population[f[1]].get_path()) + "\t:\t" + str(sum([1 for x in population[f[1]].get_path() if x==-1])))

        return population[f[1]].get_path(), f[0]


    def runAlg(self):
        self.__trace = [[1 for _ in range(self.SIZE * self.SIZE)] for _ in range(self.SIZE * self.SIZE)]
        self.__fitnessvar = []

        bestSol = []
        bestFit = 0
        for i in range(self.NR_ITER):
            sol = self.iteration()
            if sol[1] > bestFit:
                bestSol = sol[0].copy()
                bestFit = sol[1]
            if len(bestSol) == self.SIZE and -1 not in bestSol:
                break

        self.__problem.printTable(bestSol)
        print("best fitness: " + str(bestFit))

        plt.plot(self.__fitnessvar)
        plt.ylabel('fitness means')
        plt.xlabel('iterations')
        plt.show()

        return bestFit, bestSol

    def statistics(self):
        fitnesses = []
        paths = []

        for _ in range(5):
            res = self.runAlg()
            fitnesses.append(res[0])
            paths.append(res[1])

        print("\nmean of fitnesses:  \t" + str(statistics.mean(fitnesses)))
        print("stdev of fitnesses: \t" + str(statistics.stdev(fitnesses)))

        length = len(sorted(paths, key=len, reverse=True)[0])
        ind = numpy.array([xi + [numpy.nan] * (length - len(xi)) for xi in paths])
        print("mean of genotypes:  \t" + str(numpy.mean(numpy.nanmean(ind, axis=0))))
        print("stdev of genotypes: \t" + str(numpy.mean(numpy.nanstd(ind, axis=0))))



problem = Problem("problem_matrixtable.in", "problem_words.in", "problem_matrixpos.in")
controller = Controller("param.in", problem)

controller.printself()
problem.printself()

controller.statistics()
