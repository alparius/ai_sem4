import math
import random
import statistics

import matplotlib.pyplot as plt
import numpy as np

#SEED = 77
SEED = math.floor(math.pi) ** math.ceil(math.pi) - math.ceil(math.pi)


class Layer:
    """
    no neuron class is used bc we would lose the matrix multiplication advantages
    """
    def __init__(self, noInputs, noNeurons):
        self.noNeurons = noNeurons
        # init weights matrix; (0,1)*2-1 makes them be in (-1,1) - with 0 mean
        np.random.seed(SEED)
        self.weights = 2 * np.random.random((noInputs, noNeurons)) - 1
        self.output = []
        self.error = []


class Network:

    def __init__(self):
        # some constants
        self.FILENAME = "column_3C.dat"  # TODO "pregnancy.csv", "column_3C.dat", "sensor_readings_24.data"
        self.NO_HIDDENLAYERNEURONS = 12
        self.NO_HIDDENLAYERS = 4
        self.EPOCH_LIMIT = 100000
        self.LEARNING_RATE = 0.1

        # read, normalise and 'numpy-fy' data
        self.data, self.expected = self.prepare_data()
        self.TRAIN_RATIO = math.floor(len(self.data) * 80 / 100)

        # create the layers of the network
        self.layers = self.init_layers()


    @staticmethod
    def activate(x, deriv=False):
        """ sigmoid function
        :param x:
        :param deriv:
        :return:
        """
        if deriv:
            return x * (1 - x)
        return 1 / (1 + np.exp(-x))


    def train_network(self):
        """ full batch training on 80% of the data
        """
        global_error_stats = []
        refined = False
        j = 0
        while j < self.EPOCH_LIMIT and not refined:
            j += 1
            # feed forward
            layer_outputs = [self.data[:self.TRAIN_RATIO]]  # first layer output
            for i in range(1, len(self.layers)):
                output = self.activate(np.dot(layer_outputs[-1],self.layers[i].weights))
                layer_outputs.append(output)

            # get output layer error - how much did we miss the traget value
            layer_error = self.expected[:self.TRAIN_RATIO] - layer_outputs[-1]

            # mean of global output error
            global_err = np.mean(np.abs(layer_error))
            # track global error changing for statistics
            global_error_stats.append(global_err)
            # if global error is small enough, stop
            if global_err < 0.01:  # TODO
                refined = True
            if j % 100 == 0:
                print(statistics.mean(global_error_stats[-99:]))

            # get weight error differences
            error_deltas = [layer_error * self.activate(layer_outputs[-1], deriv=True)] # last layer error delta
            for i in range(len(self.layers)-2, 0, -1):
                # how much did each prev layer output value contribute to the error (according to the weights)
                layer_error = np.dot(error_deltas[-1], self.layers[i+1].weights.T)
                # if prediction is confident, dont change much (change rate depends on the slope of the sigmoid)
                error_delta = layer_error * self.activate(layer_outputs[i], deriv=True)
                error_deltas.append(error_delta)

            # update weights
            error_deltas.reverse() # reverse this so easier to iterate with i
            layer_outputs.pop()
            for i in range(len(self.layers)-1, 0, -1):
                self.layers[i].weights += self.LEARNING_RATE * np.dot(layer_outputs.pop().T, error_deltas[i-1])

        global_error_stats = [*np.array_split(global_error_stats, j/100)]
        plt.plot([statistics.mean(sub) for sub in global_error_stats])
        plt.ylabel('global error in (0,1)')
        plt.xlabel('100 iterations')
        plt.show()


    def test_network(self):
        """ testing on the other 20% of the data
        """
        # feed forward for outputs
        output = self.data[self.TRAIN_RATIO:]  # first layer output
        for i in range(1, len(self.layers)):
            output = self.activate(np.dot(output, self.layers[i].weights))

        expected = self.expected[self.TRAIN_RATIO:]
        count = 0
        # checking how many predictions were correct
        for i in range(len(output)):
            if np.mean(np.abs(output[i] - expected[i])) < 0.2:
                count += 1

        print("testing done: " + str(count) + "/" + str(len(expected)))


    def prepare_data(self):
        # read the input and output data
        data, expected = self.readData()
        # normalize the data
        self.normaliseData(data)
        # cast them into numpy matrices for hassle-free calculations
        data = np.array(data)
        expected = np.array(expected)
        return data, expected


    def readData(self):
        # output representation mapping, change this depending on the problem
        mappings = {"DH": [1.0, 0.0, 0.0], "SL": [0.0, 1.0, 0.0], "NO": [0.0, 0.0, 1.0]}
        #mappings = {"1": [1.0, 0.0, 0.0], "2": [0.0, 1.0, 0.0], "3": [0.0, 0.0, 1.0]} # for pregnancy
        #mappings = {"Slight-Right-Turn": [1.0, 0.0, 0.0, 0.0], "Sharp-Right-Turn": [0.0, 1.0, 0.0, 0.0], "Move-Forward": [0.0, 0.0, 1.0, 0.0], "Slight-Left-Turn":[0.0, 0.0, 0.0, 1.0]}

        # read all lines of the data file
        with open(self.FILENAME, "r") as file:
            content = file.readlines()
        # clean input data
        content = [line.strip().split(" ") for line in content]  # TODO .split(",")
        # shuffle input data lines
        random.seed(SEED)  # seeds are used so change effects can be tracked
        random.shuffle(content)

        inData = []
        outData = []
        for line in content:
            # pop and save the output data
            outData.append(mappings[line.pop()])
            # save the input data as floats list
            inData.append([float(elem) for elem in line])
        return inData, outData


    def normaliseData(self, trainData):
        # statistical normalisation based on data column deviation ranges
        noInputs = len(trainData[0])
        databaseSize = len(trainData)
        for j in range(noInputs):
            summ = 0.0
            for i in range(databaseSize):
                summ += trainData[i][j]
            mean = summ / databaseSize
            squareSum = 0.0
            for i in range(databaseSize):
                squareSum += (trainData[i][j] - mean) ** 2
            deviation = math.sqrt(squareSum / databaseSize)
            for i in range(databaseSize):
                trainData[i][j] = self.activate((trainData[i][j] - mean) / deviation)


    def init_layers(self):
        # create first layer with raw inputs
        layers = [Layer(noInputs=0, noNeurons=self.data.shape[1])]
        # create first hidden layer
        layers += [Layer(noInputs=self.data.shape[1], noNeurons=self.NO_HIDDENLAYERNEURONS)]
        # create hidden layers
        layers += [Layer(noInputs=self.NO_HIDDENLAYERNEURONS, noNeurons=self.NO_HIDDENLAYERNEURONS) for _ in
                   range(self.NO_HIDDENLAYERS - 1)]
        # create output layer
        layers += [Layer(noInputs=self.NO_HIDDENLAYERNEURONS, noNeurons=self.expected.shape[1])]
        return layers


network = Network()
network.train_network()
network.test_network()
