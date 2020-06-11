from tabulate import tabulate


class State(object):

    def __init__(self, table):
        self.__table = table
        self.priority = 999

    def setPriority(self, priority):
        self.priority = priority

    def getValues(self):
        return self.__table[:]

    def __str__(self):
        return tabulate(self.__table, tablefmt="grid")

    def __lt__(self, other):
        return self.priority < other.priority

    def __eq__(self, other):
        return self.priority == other.priority

