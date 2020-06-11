import time

from algorithm import Algorithm
from problem import Problem


class Application:

    @staticmethod
    def main():
        problem = Problem("data01.in")
        algoritm = Algorithm(problem, "param.in")

        #start_time = time.time()

        algoritm.statistics()

        #print("--- %s seconds ---" % (time.time() - start_time))

    # TODO Problem:
    #  Consider cubes of known sides’ length si and colors ci.
    #  Assemble thehighest pyramid from the cubes in such a way that
    #  - it has ‘stability’ (there is not a bigger cube over a smaller one)
    #  - and there are not two consecutive cubes of the same color.

    # TODO
    #   1. 1. It must have a nice architecture (follow the UML diagrams in proportion of 90% -
    #       you can add/change functions, attributes, methods or classes as need it)
    #   .
    #   2. the input data for the problem (if need it) will be in a text file ‘dataXX.in’ (XX - 01; 02; …),
    #   .
    #   3. the specific parameters (probability of mutation and crossover, population size and
    #       number of generations) ‘param.in’
    #   .
    #   4. Some specific validation tests will be performed and the results displayed on console -
    #       the average and standard deviation for the best solutions found by your the algorithm
    #       after 1000 evaluations of the fitness function in 30 runs, with populations of 40
    #       individuals.
    #   .
    #   5. A plot depicting the fitness variation during one run (use mathplotlib for this task)


Application.main()
