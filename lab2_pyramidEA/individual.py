import copy
from random import randint, random, sample, shuffle


class Individual:

    def __init__(self, cubes, premade=None):
        """
        Create a member of the population - an individual

        cubesnr: number of cubes to select from
        """
        if premade is None:
            # the number of genes (components)
            randlen = randint(2, len(cubes.keys()))
            # picking RANDLEN nr of unique cubes
            self.__genotype = sample(cubes.keys(), randlen)
            shuffle(self.__genotype)

        else:
            # individual genotype already exists, made via crossover
            self.__genotype = premade

        self.__fitness = self.__calc_fitness(cubes)


    def __str__(self):
        return str(self.__genotype)

    def __len__(self):
        return len(self.__genotype)

    def __lt__(self, other):
        if self.__fitness == other.__fitness:
            return len(self) < len(other)
        return self.__fitness < other.__fitness

    def __gt__(self, other):
        if self.__fitness == other.__fitness:
            return len(self) > len(other)
        return self.__fitness > other.__fitness

    def get_fitness(self):
        return self.__fitness

    def get_genotype(self):
        return self.__genotype

    def get_fenotype(self, cubes):
        return [cubes[i] for i in self.__genotype]


    def __calc_fitness(self, cubes):
        """
        Determine the fitness of an individual. Higher is better (maximisation problem)
        For this problem we give points if:
            - next cube is smaller than the previous
            - next cube is other color than the previous
            - subtract points otherwise
            - extra points if config is fully valid

        individual: the individual to evaluate
        cubes: dict, mapping keys to cube sizes and colors
        """
        f = 0
        good = True
        prevsize = cubes[self.__genotype[0]][0]
        prevcolor = cubes[self.__genotype[0]][1]
        itergenotype = iter(self.__genotype)
        next(itergenotype)
        for i in itergenotype:
            if cubes[i][0] <= prevsize:
                f += 1
            else:
                f -= 1
                good = False
            if cubes[i][1] != prevcolor:
                f += 1
            else:
                f -= 1
                good = False
            prevsize = cubes[i][0]
            prevcolor = cubes[i][1]

        if f > len(self):
            f += len(self)

        if good:
            f += 20

        return f


    def mutate(self, pM, cubes):
        """
        Performs a mutation on an individual with the probability of pM.
        If the event will take place, at a random position a a cube will be replaced with another random one
        individual:the individual to be mutated

        pM: the probability the mutation to occur
        cubes: dict, mapping keys to cube sizes and colors
        """
        if pM > random():
            # the position in the individual we are modifying
            randpos = randint(0, len(self) - 1)

            # if config already max size, remove that cube
            if len(self) == len(cubes):
                self.__genotype.pop(randpos)

            # else change that cube into a random one not used yet
            else:
                # the set of cubes we already used in the individual
                exclude = set(self.__genotype)
                # the list of cubes that can be added to the individual
                possible = list(set(cubes.keys()) - set(exclude))
                # selecting the new cube to be added in place of the one we are replacing
                randnewcube = randint(0, len(possible) - 1)
                # the replace happening
                self.__genotype[randpos] = possible[randnewcube]

        # genotype changed, recalculate fitness
        self.__fitness = self.__calc_fitness(cubes)


    @staticmethod
    def crossover1(parent1, parent2, cubes):
        """
        crossover between 2 parents
        a new arrangement of cubes with random length and random cubes of parents

        cubes: dict, mapping keys to cube sizes and colors
        """
        # we take the first half of the first parent
        firsthalf = parent1.__genotype[len(parent1)//2 : ]
        # and the second part of the second parent
        secondhalf = parent2.__genotype[ : len(parent2)//2]
        # and merge them
        child = firsthalf + secondhalf
        # then remove duplicates
        child = list(dict.fromkeys(child))
        # create the new child from the genotype
        i3 = Individual(cubes, premade=child)
        return i3


    @staticmethod
    def crossover2(parent1, parent2, cubes):
        """
        crossover between 2 parents
        a new arrangement of cubes with random length and random cubes of parents

        cubes: dict, mapping keys to cube sizes and colors
        """
        child = []
        for k in range(len(parent1.__genotype)//2):
            child.append(parent1.__genotype[k])
        for k in range(len(parent2.__genotype)//2,len(parent2.__genotype)):
            child.append(parent2.__genotype[k])
        child = list(dict.fromkeys(child))
        i3 = Individual(cubes, premade=child)

        return i3


    @staticmethod
    def crossover3(parent1, parent2, cubes):
        """
        crossover between 2 parents
        a new arrangement of cubes with random length and random cubes of parents

        cubes: dict, mapping keys to cube sizes and colors
        """
        child = []

        # swap parents if first is shorter for easier handling
        if len(parent1) < len(parent2):
            parent1, parent2 = parent2, parent1

        # difference of parent lengths
        diff1 = len(parent1) - len(parent2)

        # add the first DIFF1 nr of genes to child from the longer parent
        for i in range(diff1):
            child.append(parent1.__genotype[i])

        # add the rest in merge order, only the uniques
        for i in range(len(parent2)):
            if parent1.__genotype[i + diff1] not in child:
                child.append(parent1.__genotype[i + diff1])
            if parent2.__genotype[i] not in child:
                child.append(parent2.__genotype[i])

        # trim genotype length to a random length between the parents' lengths
        randlength = randint(len(parent2), len(parent1))
        diff2 = len(child) - randlength

        # remove DIFF2 nr of random genes from new child
        for _ in range(diff2):
            randpos = randint(0, len(child) - 1)
            child.pop(randpos)

        # calculate new child fitness and return it
        i3 = Individual(cubes, premade=child)

        return i3

