import matplotlib.pyplot as plt
from statistics import mean

from my_chromosome import Chromosome
from my_population import Population


class GPAlgorithm:
    def __init__(self):
        self.FILE = "slump_test.data"
        self.POP_SIZE = 500
        self.ITERS = 200
        self.P_MUTATE = 0.8

        self.DATA_SIZE = 0
        self.inputs = []
        self.outputs = []

        self.population = Population(self.POP_SIZE)


    def run(self):
        fitnessmeans = []
        # loading and normalizing data from file
        self.loadData()
        self.normalizeData()
        # initial evaluation of the randomized population
        self.population.evaluate(self.inputs, self.outputs)

        for i in range(self.ITERS):
            print("#" + str(i) + " iteration")
            self.iteration()
            best = self.population.individuals[0]
            fitnessmeans.append(mean([ind.fitness for ind in self.population.individuals]))
            print("Best: " + str(best) + "\n" + "fitness: " + str(best.fitness))

        plt.plot(fitnessmeans)
        plt.ylabel('global error')
        plt.xlabel('iterations')
        plt.show()


    def iteration(self):
        nrChildren = self.POP_SIZE // 2
        offspring = Population(nrChildren)
        for i in range(nrChildren):
            offspring.individuals[i] = Chromosome.crossover(self.population.individuals[i << 1],
                                                            self.population.individuals[(i << 1) | 1])
            offspring.individuals[i].mutation(self.P_MUTATE)
        offspring.evaluate(self.inputs, self.outputs)
        self.population.reunion_selection(offspring)


    def loadData(self):
        with open(self.FILE, "r") as file:
            for line in file.readlines():
                values = line.strip().split(",")
                values = [float(v) for v in values]
                # an index and 7 input attribute; and only the last output is used
                self.inputs.append(values[1:8])
                # values.pop()
                # values.pop()
                self.outputs.append(values[-1])
                self.DATA_SIZE += 1
        print(str(self.DATA_SIZE) + " rows of data loaded\n")

        # for row in self.inputs:
        #     print(str(row))


    def normalizeData(self):
        minimums = self.inputs[0][:]
        maximums = self.inputs[0][:]
        for data in self.inputs:
            for i in range(len(data)):
                if data[i] < minimums[i]:
                    minimums[i] = data[i]
                elif data[i] > maximums[i]:
                    maximums[i] = data[i]

        for i in range(len(self.inputs)):
            for j in range(len(self.inputs[0])):
                self.inputs[i][j] = ( self.inputs[i][j] - minimums[j] ) / ( maximums[j] - minimums[j] )


        minimum = self.outputs[0]
        maximum = self.outputs[0]
        for data in self.outputs:
            if data < minimum:
                minimum = data
            elif data > maximum:
                maximum = data

        for i in range(len(self.outputs)):
            self.outputs[i] = ( self.outputs[i] - minimum ) / ( maximum - minimum )
