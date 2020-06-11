from random import random


class Neuron:
    def __init__(self, noInputs=0):
        self.noInputs = noInputs
        # MIN_W = -1, MAX_W = 1 - weights between [-1,1]
        self.weights = [(random() * 2 - 1) for _ in range(self.noInputs)]
        self.output = 0
        self.err = 0

    def activate(self, info):
        net = 0.0
        for i in range(self.noInputs):
            net += info[i] * self.weights[i]
        self.output = net  # for linear activation
        # self.output = 1 / (1.0 + exp(-net));	#TODO for sigmoidal activation

    def setErr(self, val):
        self.err = val  # for linear activation
        # self.err = self.output * (1 â self.output) * val #TODO for sigmoidal activation


class Layer:
    def __init__(self, noNeurons=0, noInputs=0):
        self.noNeurons = noNeurons
        self.neurons = [Neuron(noInputs) for _ in range(self.noNeurons)]
