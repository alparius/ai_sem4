from my_chromosome import Chromosome


class Population:
    def __init__(self, pop_size):
        self.pop_size = pop_size
        self.individuals = [Chromosome() for _ in range(pop_size)]

    def evaluate(self, input_train, output_train):
        for chromosome in self.individuals:
            chromosome.evaluate(input_train, output_train)

    def reunion_selection(self, offspring):
        self.individuals += offspring.individuals
        self.individuals = sorted(self.individuals, key=lambda x: x.fitness)
        print([x.fitness for x in self.individuals])
        self.individuals = self.individuals[:self.pop_size]

