import copy
import numpy
from random import *


class Ant:

    def __init__(self, size, positions, words, table):
        """ the road constructed by an ant which is initialised
        on the first position of the crossword with a random word that fits there
        the road is a permutation of 34 integers,
        each nr representing a word that goes into the i-th place in the puzzle
        :param size: size of the final permutation
        :param positions: map op CrosswordPos items
        :param words: mapping of integers to words
        :param table: the crossword table
        """
        self.size = size
        self.path = []
        self.table = table

        # adding the starting random word
        self.path.append(choice(self.nextMoves(positions, words)))

        # adding it to the table
        # (constructing the fenotype at each step to reduce complexity)
        self.addLastToTable(positions, words)


    def get_path(self):
        return self.path


    def fitness(self):
        """ maximisation problem
        the fitness depends on the nr of empty fields in the table
        :return: the fitness (between 2 and 160)
        """
        value = 0
        for row in self.table:
            count = sum(1 for e in row if e == 0)
            value += count

        rowlen = len(self.table[0])
        fitn = rowlen*rowlen - value - 65
        #if fitn > 130:
        #    fitn *= 10
        return fitn


    def nextMoves(self, positions, words):
        """ return a list of next possible moves
        trying to insert all the matching length words
        the ones that could fit, we add to a list of possible next moves
        :param positions: map op CrosswordPos items
        :param words: mapping of integers to words
        :return: a list of integers
        """
        possible = []
        nextWord = len(self.path) + 1
        nextPos = positions[nextWord]
        for key in words:
            thisword = list(words[key])
            if len(thisword) == nextPos.length:
                if int(key-1) not in self.path:
                    good = True

                    for index in range(nextPos.length):
                        if nextPos.horizontal:
                            if self.table[nextPos.x][nextPos.y + index] != 0:
                                if self.table[nextPos.x][nextPos.y + index] != thisword[index]:
                                    good = False
                        else:
                            if self.table[nextPos.x + index][nextPos.y] != 0:
                                if self.table[nextPos.x + index][nextPos.y] != thisword[index]:
                                    good = False
                    if good:
                        possible.append(key - 1)

        return possible


    def distMove(self, i):
        """ heuristic of a step
        NO HEURISTIC YET
        :param i: the index of the word to be evaluated
        """
        return 1


    def addMove(self, positions, words, trace, alpha, beta, q0):
        """ adding a new position to the ant's path, if possible
        :param positions: map op CrosswordPos items
        :param words: mapping of integers to words
        :param trace: the matrix of pheromones
        :param alpha: constant - trail importance
        :param beta: constant - visibility (empirical distance) importance
        :param q0: randomity threshold constant
        :return: ant path is updated
        """

        # we determine the possible next steps
        nextSteps = self.nextMoves(positions, words)

        # if we have no valid steps, return
        if len(nextSteps) == 0:
            #self.path.append(-1)
            return

        # if we only have a single possible step, we add it
        if len(nextSteps) == 1:
            self.path.append(nextSteps[0])
            self.addLastToTable(positions, words)
            return

        # invalid positions will be marked with 0
        p = [0 for _ in range(self.size)]

        # in the place of valid positions, we put their empirical distances
        for i in nextSteps:
            p[i] = self.distMove(i)

        # we calculate the trace^alpha and visibility^beta products
        #p = [(p[i] ** beta) * (trace[self.path[-1]][i] ** alpha) for i in range(len(p))]
        p = [(p[i] ** beta) * (trace[i][len(self.path)] ** alpha) for i in range(len(p))]
        #print([x for x in p if x])

        if random() < q0:
            # we add the best possible next move
            p = [[i, p[i]] for i in range(len(p))]
            p = max(p, key=lambda a: a[1])
            self.path.append(p[0])
            self.addLastToTable(positions, words)
            return

        else:
            s = sum(p)
            if s == 0:
                self.path.append(choice(nextSteps))
                self.addLastToTable(positions, words)
                return
            # we select the next move by monte carlo selection
            p = [[i, p[i]/s] for i in range(len(p))]
            p = [x for x in p if x[1]!=0]
            draw = numpy.random.choice([x[0] for x in p], 1, p=[x[1] for x in p])
            self.path.append(draw[0])
            self.addLastToTable(positions, words)
            return


    def addLastToTable(self, positions, words):
        """ adding the last inserted word to the table
        :param positions: map op CrosswordPos items
        :param words: mapping of integers to words
        :return: the fenotype is modified
        """
        word = list(words[self.path[-1] + 1])
        wordpos = positions[len(self.path)]
        for index in range(wordpos.length):
            if wordpos.horizontal:
                self.table[wordpos.x][wordpos.y + index] = word[index]
            else:
                self.table[wordpos.x + index][wordpos.y] = word[index]
