import copy

from individual import Individual


class Population:

    def __init__(self, size, cubes):
        self.__size = size
        self.__cubes = cubes
        self.__list = []

        for _ in range(self.__size):
            i = Individual(self.__cubes)
            self.__list.append(i)


    def evaluate(self):
        graded = self.__list
        graded = sorted(graded, reverse=True)
        return graded[0]

    #def selection(self, params):
    #    return

    def get_list(self):
        return self.__list
