import heapq

class Controller:

    def __init__(self, problem):
        self.__problem = problem


    def BreadthFirstSearch(self):
        q = [self.__problem.getRoot()]
        while len(q) > 0:
            currentState = q.pop()
            if self.__problem.checkSolution(currentState):
                return currentState
            q += self.__problem.expand(currentState)
        raise ValueError("no solution")


    def BestFirstSearch(self):
        priorq = []
        heapq.heappush(priorq, self.__problem.getRoot())
        while len(priorq) > 0:
            currentState = heapq.heappop(priorq)
            #print(currentState.priority)
            if self.__problem.checkSolution(currentState):
                return currentState
            for aux in self.__problem.expand(currentState):
                aux.setPriority(self.__problem.heuristics(aux))
                heapq.heappush(priorq, aux)
        raise ValueError("no solution")


    '''
    def BestFirstSearch(self):
        priorq = [(self.__problem.getRoot(),1)]
        while len(priorq) > 0:
            currentState = priorq.pop()[0]
            if self.__problem.checkSolution(currentState):
                return currentState
            for x in self.__problem.expand(currentState):
                x.setPriority(self.__problem.heuristics(x))
                priorq.append((x, x.priority))
            priorq.sort(key=lambda x: x[1])
        raise ValueError("no solution")

    #
    '''
