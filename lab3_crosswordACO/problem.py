import copy

from CrosswordPos import CrosswordPos


class Problem:

    def __init__(self, matrixfile, wordsfile, posfile):
        self.load(matrixfile, wordsfile, posfile)

    def load(self, matrixfile, wordsfile, posfile):
        with open(matrixfile, "r") as file:
            self.__table = [[int(x) for x in ln.split()] for ln in file]

        with open(wordsfile, "r") as file:
            nr = int(file.readline().strip())
            self.__words = {}
            for i in range(nr):
                self.__words[i+1] = file.readline().strip()

        with open(posfile, "r") as file:
            nr2 = int(file.readline().strip())
            self.__positions = {}
            for i in range(nr):
                line = file.readline().strip().split(" ")
                pos = CrosswordPos(int(line[0]), int(line[1]), int(line[2]), int(line[3]), int(line[4]))
                self.__positions[i+1] = pos


    def get_positions(self):
        return copy.deepcopy(self.__positions)

    def get_words(self):
        return self.__words

    def get_table(self):
        return copy.deepcopy(self.__table)


    def printTable(self, solution):
        i = 0
        table = self.get_table()
        for pos in solution:
            i += 1
            if pos == -1:
                continue
            word = list(self.__words[pos + 1])
            wordpos = self.__positions[i]

            for index in range(wordpos.length):
                if wordpos.horizontal:
                    table[wordpos.x][wordpos.y + index] = word[index]
                else:
                    table[wordpos.x + index][wordpos.y] = word[index]


        for row in table:
            for elem in row:
                if elem == 1:
                    print("\t█", end='')
                elif elem == 0:
                    print("\t ", end='')
                else:
                    print("\t" + str(elem), end='')
            print("")


    def printself(self):
        for key in self.__words:
            print("#" + str(key) + ": " + str(self.__words[key]))

        print("")

        table = self.get_table()
        for pos in list(self.__positions.values()):
            pos.printself()
            table[pos.x][pos.y] = "X"

        for row in table:
            for elem in row:
                if elem == 1:
                    print("\t█", end='')
                elif elem == 0:
                    print("\tO", end='')
                else:
                    print("\tX", end='')
            print("")

        print("")
