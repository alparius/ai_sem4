import itertools

from FuzzyFigures import FuzzyVariable, FuzzyTable


class FuzzySystem:
    def __init__(self):
        self.in_texture = FuzzyVariable()
        self.in_capacity = FuzzyVariable()
        self.out_cycletype = FuzzyVariable()
        self.rules = FuzzyTable()
        self.load_problem()


    def compute(self, texture, capacity):
        """ use the fuzzy RBS to compute teh results for an input
        :param texture, capacity: input float values for the fuzzy RBS
        :return: the defuzzified cycle type as a float
        """
        fuzzy_texture = self.in_texture.fuzzify(texture)
        fuzzy_capacity = self.in_capacity.fuzzify(capacity)

        # TODO test print
        print("\ntexture membership degrees in the fuzzy regions:")
        print([str(k + ": " + "%.2f" % v) for k, v in fuzzy_texture.items()])
        print("\ncapacity membership degrees in the fuzzy regions:")
        print([str(k + ": " + "%.2f" % v) for k, v in fuzzy_capacity.items()])

        # evaluate all rule values for the all the regions
        rule_values = [self.rules.evaluate_rule(p1,p2) for p1 in fuzzy_texture.items() for p2 in fuzzy_capacity.items()]

        # keep only the best value of each region
        best_values = [i for i in rule_values if i[1]==max([k[1] for k in rule_values if k[0]==i[0]])]

        # TODO test print
        print("\nfuzzy rule values:")
        print([str(i[0] + ": " + "%.2f" % i[1]) for i in best_values])

        weighted_total = 0
        weight_sum = 0
        for region,weight in rule_values:
            weight_sum += weight
            weighted_total += self.out_cycletype.middleof_region(region) * weight
        return weighted_total / weight_sum


    def load_problem(self):
        with open("problem.in", "r") as file:
            for _ in range(4):
                line = file.readline().strip().split(" ")
                self.in_texture.add_region(name=line[0], params=(float(line[1]), float(line[2]), float(line[3]) ,float(line[4])))
            file.readline()

            for _ in range(3):
                line = file.readline().strip().split(" ")
                self.in_capacity.add_region(name=line[0], params=(float(line[1]), float(line[2]), float(line[3]), float(line[4])))
            file.readline()

            for _ in range(4):
                line = file.readline().strip().split(" ")
                self.out_cycletype.add_region(name=line[0], params=(float(line[1]), float(line[2]), float(line[3]), float(line[4])))
            file.readline()

            for _ in range(12):
                line = file.readline().strip().split(" ")
                self.rules.add_rule(texture=line[0], capacity=line[1], cycletype=line[2])

        # TODO test print
        print("texture regions:")
        print(str(self.in_texture))
        print("capacity regions:")
        print(str(self.in_capacity))
        print("cycletype regions:")
        print(str(self.out_cycletype))
        print("fuzzy rules:")
        print(str(self.rules))
