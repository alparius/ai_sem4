from math import exp

from Neuron import Layer

LEARN_RATE = 0.1
EPOCH_LIMIT = 1000


class Network:
    def __init__(self, noInputs=0, noOutputs=0, noHiddenLayers=0, noNeuronsPerHiddenLayer=0):
        self.noInputs = noInputs
        self.noOutputs = noOutputs
        self.noHiddenLayers = noHiddenLayers
        self.noNeuronsPerHiddenLayer = noNeuronsPerHiddenLayer
        # input layer
        self.layers = [Layer(noNeurons=self.noInputs, noInputs=0)]
        # first hidden layer has noInputs inputs exactly
        self.layers += [Layer(noNeurons=self.noNeuronsPerHiddenLayer, noInputs=self.noInputs)]
        # additional hidden layers have as many inputs as neurons
        self.layers += [Layer(noNeurons=self.noNeuronsPerHiddenLayer, noInputs=self.noNeuronsPerHiddenLayer) for _ in range(self.noHiddenLayers - 1)]
        # output layer
        self.layers += [Layer(noNeurons=self.noOutputs, noInputs=self.noNeuronsPerHiddenLayer)]

    def activate(self, inputs):
        i = 0
        # activate input layer, its output is just the input
        for neuron in self.layers[0].neurons:
            neuron.output = inputs[i]
            i += 1
        # activate the rest of the layers
        for noLayer in range(1, self.noHiddenLayers + 1):
            # get the output array of the previous layer
            prevLayerOutput = []
            noInputs = len(self.layers[noLayer-1].neurons)
            for i in range(noInputs):
                prevLayerOutput.append(self.layers[noLayer - 1].neurons[i].output)
            # activate all the neurons of this layer with the prev output array
            for neuron in self.layers[noLayer].neurons:
                neuron.activate(prevLayerOutput)

    def errorsBackpropagate(self, err):
        # from last layer towards first
        for layer in range(self.noHiddenLayers + 1, 1, -1):
            i = 0
            for neuron in self.layers[layer].neurons:
                if layer == self.noHiddenLayers + 1:
                    # last layer error calc
                    neuron.setErr(err[i])
                else:
                    sumErr = 0.0
                    for prevLayerNeuron in self.layers[layer + 1].neurons:
                        sumErr += prevLayerNeuron.weights[i] * prevLayerNeuron.err
                    neuron.err = sumErr
                for j in range(neuron.noInputs):
                    netWeight = neuron.weights[j] + LEARN_RATE * neuron.err * self.layers[layer - 1].neurons[j].output
                    neuron.weights[j] = netWeight
                i += 1
    '''
    def errorComputationRegression(self, target, err):
        # return the output layer global error for a regression problem
        globalErr = 0.0
        for i in range(self.layers[self.noHiddenLayers + 1].noNeurons):
            err.append(target[i] - self.layers[self.noHiddenLayers + 1].neurons[i].output)
            globalErr += err[i] * err[i]
        return globalErr
    '''

    def errorComputationClassification(self, target, noLabels):
        # normalise the output of neurons from the output layer (softmax transformation;
        # sum of transformed outputs is 1, each transformed output behaves like a probability)
        '''
        transfOutputs = []
        # getting the maximum of the outputs from last layer
        maxx = self.layers[self.noHiddenLayers + 1].neurons[0].output
        for i in range(noLabels):
            if self.layers[self.noHiddenLayers + 1].neurons[i].output > maxx:
                maxx = self.layers[self.noHiddenLayers + 1].neurons[i].output
        # getting exponential sum of outputs' differences w.r.t. max
        sumExp = 0.0
        for i in range(noLabels):
            sumExp += exp(self.layers[self.noHiddenLayers + 1].neurons[i].output - maxx)
        # collecting the output difference
        for i in range(noLabels):
            transfOutputs.append(exp(self.layers[self.noHiddenLayers + 1].neurons[i].output - maxx) / sumExp)
        maxx = transfOutputs[0]
        print(transfOutputs)

        computedlabel = 1
        for i in range(1, noLabels):
            if transfOutputs[i] > maxx:
                maxx = transfOutputs[i]
                computedlabel = i + 1
        if len(err) == 0:
            err.append(-1)
        if target == computedlabel:
            err[0] = 0
        else:
            err[0] = 1
        globalErr = err[0]
        return globalErr
        '''
        error = []
        for i in range(noLabels):
            diff = self.layers[self.noHiddenLayers + 1].neurons[i].output - target[i]
            error.append(diff)
        return error


    @staticmethod
    def checkGlobalErr(err):
        '''
        # regression
        error = sum(err)
        if abs(error) < 1 / (10 ** 8):
            return True
        else:
            return False
        '''   
        # classification
        correct = sum(err)
        error = correct/len(err)
        return False
        if error > 0.9:
            return True
        else:
            return False

    def learning(self, inData, outData):
        stopCondition = False
        epoch = 0
        while (not stopCondition) and (epoch < EPOCH_LIMIT):
            globalErr = []
            # for each training example
            for dat in range(len(inData)):
                self.activate(inData[dat])  # activate all the neurons; propagate forward the signal
                err = self.errorComputationClassification(outData[dat], 3)
                # backpropagate the error of neurons from the output layer
                #globalErr[dat] = self.errorComputationRegression(outData[dat], err)
                globalErr.append(sum([1 for i in err if i != 0]))
                self.errorsBackpropagate(err)
            stopCondition = self.checkGlobalErr(globalErr)
            print(sum(globalErr))
            epoch += 1

    def testing(self, inData, outData):
        globalErr = []
        for dat in range(len(inData)):  # for each testing example
            self.activate(inData[dat])  # activate all the neurons; propagate forward the signal
            err = self.errorComputationClassification(outData[dat], 3)
            # compute the error of neurons from the output layer
            #globalErr[d] = self.errorComputationRegression(outData[d], err)
            globalErr.append(sum([1 for i in err if i != 0]))
        print(len(globalErr))
