import collections
import statistics
from math import sqrt
import numpy
import copy

from State import State

'''
SUDOKU - a logic puzzle represented on a NxN board
some squares already contain a number, others must be completed with other numbers from {​ 1,2,…,n ​ }
in such a way that each line, column and square with the edge equal with √n must contain only different numbers.
Determine one correct solution for the puzzle. 
  
'''

class Problem:

    def __init__(self, root):
        self.__root = root
        self.__size = self.__root.getValues().shape[0]
        self.__sizesqrt = int(sqrt(self.__size))
        self.__complete = set(list(range(1, self.__size + 1)))

    def getRoot(self):
        return self.__root


    @staticmethod
    def readfile(filename):
        data = numpy.loadtxt(filename)
        return State(data)


    def expand(self, state):
        mat = state.getValues()
        newstates = []
        for i in range(self.__size):
            for j in range(self.__size):
                if mat[i][j] == 0:
                    for k in range(self.__size):
                        newmat = copy.deepcopy(mat)
                        newmat[i][j] = k+1
                        newstates.append(State(newmat))
                    return newstates
        return newstates


    def heuristics(self, state):
        first_criteria = self.__size * self.__size - numpy.count_nonzero(state.getValues())

        arr1 = state.getValues().flatten()
        arr2 = arr1[arr1 != 0]
        second_criteria = numpy.var(arr2)

        #counts = numpy.unique(state.getValues(), return_counts=True)[1]
        #if len(counts)==5:
        #    counts = numpy.delete(counts, 0)
        #second_criteria = numpy.var(counts)

        #arr1 = list(state.getValues().flatten())
        #counts = list(collections.Counter(arr1).values())
        #if len(counts)==5:
        #    counts.pop(0)
        #second_criteria = statistics.pvariance(counts)


        return first_criteria * 100 - second_criteria
        #return 100 - second_criteria


    def checkSolution(self, state):
        mat = state.getValues()

        if (numpy.count_nonzero(mat)) != self.__size * self.__size:
            return False

        occurences = []
        for i in range(1,self.__size+1):
            occurences.append(numpy.count_nonzero(mat == i))
        if set(occurences) != {self.__size}:
            return False

        for row in mat:
            if set(row) != self.__complete:
                return False

        for column in mat.transpose():
            if set(column) != self.__complete:
                return False

        for i in range(self.__size, self.__sizesqrt):
            for j in range(self.__size, self.__sizesqrt):
                square = list(numpy.itertools.chain(row[j:j + self.__sizesqrt] for row in mat[i:i + self.__sizesqrt]))
                if set(square) != self.__complete:
                    return False

        return True