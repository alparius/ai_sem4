"""
TODO
    Specify, design and deploy an application in python that solve your assigned problem with a Ruled Based System in
    uncertain environments (fuzzy). The applications should follow the following conditions:
        1. it must have a nice layered architecture of MCV type
        2. the input data for the problem (if need it) will be in a text file ‘problem.in’ (will contain the
            parameters for the fuzzy classes),
        3. the input data for the system will be in ‘input.in’ and the output in the file ‘output.out’ also
            the inputs and the results will be printed on console
        4. a short description of the chosen method will be in the file ‘description.txt’, this file will
            describe the algorithm and the chosen model (Mamdani or Sugeno), and other specific
            info, as well as the validation for the results (for 2 inputs a CLEAR calculation for the
            result going through ALL the steps of the method)

TODO
    3. The washing machine
    Design and implement a control module to adjust the washing cycle for a washing machine.
    The wash cycle (delicate, easy, normal, intense) depends
        on the texture of clothes (very soft, soft, normal, resistant) and
        on the amount of clothes loaded in the car (small, medium, high).
"""

from FuzzySystem import FuzzySystem


class Application:
    def __init__(self):
        self.system = FuzzySystem()

    def compute(self, texture, capacity):
        return self.system.compute(texture, capacity)

    def run(self):
        with open("input.in", "r") as inputfile, open("output.out", "w") as outputfile:
            for line in inputfile.readlines():
                line = line.strip().split(" ")
                result = self.compute(texture=float(line[0]), capacity=float(line[1]))

                print("\nif the texture is: " + line[0] + " and the capacity is: " + line[1] +
                      " then the cycle type needs to be: " + str("%.2f" % result) + "\n\n")

                outputfile.write("texture=" + line[0] + " and capacity=" + line[1] + " --> cycletype=" +str("%.2f" % result) + "\n")


app = Application()
app.run()
