class FuzzyVariable:
    """ values and changing of a fuzzy variable
    contains parameters for the membership functions for each fuzzy region
    """
    def __init__(self):
        self.regions = {}

    def __str__(self):
        string = ""
        for k,v in self.regions.items():
            string += str(k) + ": " + str(v) + "\n"
        return string

    def add_region(self, name, params):
        """ adding a region with parameters for a trapezoidal membership function
        :param name: name of the region
        :param params: parameters of the region (tuple of a, b, c, d floats)
        :return: the region is added to the fuzzy variable
        """
        self.regions[name] = params

    @staticmethod
    def trapezoid(x, a, b, c, d):
        """ fuzzifies a value using the trapezoidal membership function:
        max(0, min((x - a) / (b - a)), 1, ((d - x) / (d - c))
        :param x: the float value to be fuzzified
        :param a, b, c, d: float parameters of the trapezoidal membership function
        :return: the membership degree of the value wrt to the region
        """
        first = 999.9 if (b-a)==0.0 else (x-a)/(b-a)
        second = 999.9 if (d-c)==0.0 else (d-x)/(d-c)
        return max(0.0, min(first, 1.0, second))

    def fuzzify(self, value):
        """ return the fuzzified values for each region
        :param value: the value to be fuzzified
        :return: a (string -> float) mapping between region names and membership degrees
        """
        return { k: self.trapezoid(value, *v) for k,v in self.regions.items() }

    def middleof_region(self, region):
        """ return the mean of a region for weighted average calculation
        :param region: name of the region
        :return: the middle point of the region
        """
        r = self.regions[region]
        return (r[3] + r[0]) / 2


class FuzzyTable:
    """ values for a table of conjunctive fuzzy rules
        texture AND capacity  => cycletype
    """
    def __init__(self):
        self.rules = {}

    def __str__(self):
        string = ""
        for k,v in self.rules.items():
            string += str(k) + ": " + str(v) + "\n"
        return string

    def add_rule(self, texture, capacity, cycletype):
        """ adds a rule to the set of fuzzy rules
        :param texture, capacity: input fuzzy region names
        :param cycletype: output fuzzy region name
        :return: the rule is added as a mapping
        """
        self.rules[(texture, capacity)] = cycletype

    def evaluate_rule(self, texture, capacity):
        """ evaluates a fuzzy rule
        :param texture, capacity: tuples of fuzzy region names and membership degrees
        :return: tuple of the output fuzzy region name and the minimum of the membership degrees conforming the Sugeno model
        """
        return [self.rules[(texture[0], capacity[0])], min(texture[1],capacity[1])]
