from random import randint, random

MAX_DEPTH = 4
terminals = ['cement', 'slag', 'fly_ash', 'water', 'sp', 'coarse_aggr', 'fine_aggr']
noTerminals = 7
functions = ['+', '-', '*', '/']
noFunctions = 4


class Chromosome:
    def __init__(self):
        self.fitness = 0
        self.size = 0
        self.repres = [0 for _ in range(2 ** (MAX_DEPTH + 1) - 1)]
        self.init_tree()

    def __str__(self):
        fenotype = list(self.repres)
        for i in range(len(fenotype)):
            if fenotype[i] < 0:
                fenotype[i] = functions[- fenotype[i] - 1]
            else:
                fenotype[i] = terminals[fenotype[i] - 1]
        return str(fenotype)


    def evaluate(self, in_data, out_data):
        """ the fitness function
        """
        err = 0.0
        for (x, y) in zip(in_data, out_data):
            err += abs(y - self.eval_expression(0, x)[0])
            #print(str(y)  + " : " + str(self.eval_expression(0, x)[0]))
        self.fitness = err / len(in_data)
        # self.fitness = err

    def eval_expression(self, pos, row_data):
        """ the expresion value for some specific terminals
        """
        if self.repres[pos] > 0:  # a terminal
            return row_data[self.repres[pos] - 1], pos

        elif self.repres[pos] < 0:  # a function
            if functions[-self.repres[pos] - 1] == '+':
                aux_1 = self.eval_expression(pos + 1, row_data)
                aux_2 = self.eval_expression(aux_1[1] + 1, row_data)
                return aux_1[0] + aux_2[0], aux_2[1]

            elif functions[-self.repres[pos] - 1] == '-':
                aux_1 = self.eval_expression(pos + 1, row_data)
                aux_2 = self.eval_expression(aux_1[1] + 1, row_data)
                return aux_1[0] - aux_2[0], aux_2[1]

            elif functions[-self.repres[pos] - 1] == '*':
                aux_1 = self.eval_expression(pos + 1, row_data)
                aux_2 = self.eval_expression(aux_1[1] + 1, row_data)
                return aux_1[0] * aux_2[0], aux_2[1]

            elif functions[-self.repres[pos] - 1] == '/':
                aux_1 = self.eval_expression(pos + 1, row_data)
                aux_2 = self.eval_expression(aux_1[1] + 1, row_data)
                if aux_2[0] == 0:
                    return aux_1[0] , aux_2[1]
                return aux_1[0] / aux_2[0], aux_2[1]


    def init_tree(self, pos=0, depth=0):
        """ initialise randomly an expression
        """
        if depth < MAX_DEPTH:
            if random() < 0.5:
                self.repres[pos] = randint(1, noTerminals)
                self.size = pos + 1
                return pos + 1
            else:
                self.repres[pos] = - randint(1, noFunctions)
                finalFirstChild = self.init_tree(pos + 1, depth + 1)
                finalSecondChild = self.init_tree(finalFirstChild, depth + 1)
                return finalSecondChild
        else:
            # choose a terminal
            self.repres[pos] = randint(1, noTerminals)
            self.size = pos + 1
            return pos + 1


    def traverse(self, pos):
        """ returns the next index where it begins the next
        branch in the tree from the same level
        """
        if self.repres[pos] > 0:  # terminal
            return pos + 1
        else:
            return self.traverse(self.traverse(pos + 1))


    def mutation(self, probability):
        if random() < probability:
            off = Chromosome()
            off.repres = self.repres[:]
            off.size = self.size
            for _ in range(2):
                pos = randint(0, self.size-1)
                if off.repres[pos] > 0:  # terminal
                    off.repres[pos] = randint(1, noTerminals)
                else:  # function
                    off.repres[pos] = -randint(1, noFunctions)
            return off
        else:
            return self


    @staticmethod
    def crossover(first, second):
        off = Chromosome()
        while True:
            start_first = randint(0, first.size - 1)
            end_first = first.traverse(start_first)
            start_second = randint(0, second.size - 1)
            end_second = second.traverse(start_second)
            if len(off.repres) > end_first + (end_second - start_second - 1) + (first.size - end_first - 1):
                break
        i = -1
        for i in range(start_first):
            off.repres[i] = first.repres[i]
        for j in range(start_second, end_second):
            i = i + 1
            off.repres[i] = second.repres[j]
        for j in range(end_first, first.size):
            i = i + 1
            off.repres[i] = first.repres[j]
        off.size = i + 1
        # print(str(first))
        # print(str(second))
        # print(str(off))
        # print(str("--------------"))
        return off
