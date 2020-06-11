import copy


class Problem:

    def __init__(self, problemfile):
        self.load(problemfile)

    def load(self, problemfile):
        file2 = open(problemfile, "r")
        nrcubes = int(file2.readline().strip())
        self.__cubes = {}
        for i in range(nrcubes):
            line = file2.readline().strip().split(" ")
            self.__cubes[i+1] = ( int(line[0]), int(line[1]) )
        file2.close()

        print("\nset of cubes: " + str(list(self.__cubes.values())) + "\n")


    def get_cubes(self):
        return copy.deepcopy(self.__cubes)
