import copy
from math import sqrt

import numpy as np


def nonlin(x, deriv=False):
    """ sigmoid function and its derivative
    RENAME THIS
    """
    if deriv:
        return x * (1 - x)
    return 1 / (1 + np.exp(-x))




    # * elementwise multiplication
    # -+ elementwise on matrix
    # dot - matrix mul



def dostuff():
    """ getting input and output data
    each row is a data example
    no neuron classes bc then no matrixmul
    """
    X, y = readData()

    # same seed bc input and output needs to remain in order
    np.random.seed(42)
    np.random.shuffle(X)
    np.random.seed(42)
    np.random.shuffle(y)

    # randomly initialize our weights with mean 0
    # creating random numbers between (0,1)*2-1 makes them be in (-1,1)
    # seed so improvements changes effect can be easily seen
    #np.random.seed(42)
    weights0 = 2 * np.random.random((6, 8)) - 1
    #np.random.seed(42)
    weights1 = 2 * np.random.random((8, 8)) - 1
    #np.random.seed(42)
    weights2 = 2 * np.random.random((8, 8)) - 1
    #np.random.seed(42)
    weights3 = 2 * np.random.random((8, 2)) - 1

    stop = False # when globalerror is small enough
    j = 0
    # full batch training
    while j < 100000 and not stop:

        # Feed forward through layers 0, 1, and 2
        l0 = X # first layer is input
        l1 = nonlin(np.dot(l0, weights0))
        l2 = nonlin(np.dot(l1, weights1))
        l3 = nonlin(np.dot(l2, weights2))
        l4 = nonlin(np.dot(l3, weights3))

        # how much did we miss the target value?
        l4_error = y - l4

        # replace this with collecting data and plot
        if (j % 3333) == 0:
            print("Error:" + str(np.mean(np.abs(l4_error))))

        # in what direction is the target value?
        # were we really sure? if so, don't change too much.
        # (change rate depends on the slope of the sigmoid)
        l4_delta = l4_error * nonlin(l4, deriv=True)

        # how much did each prev layer output value contribute to the l2 error (according to the weights)?
        l3_error = np.dot(l4_delta, weights3.T)

        l3_delta = l3_error * nonlin(l3, deriv=True)
        l2_error = np.dot(l3_delta,weights2.T)
        l2_delta = l2_error * nonlin(l2, deriv=True)
        l1_error = np.dot(l2_delta,weights1.T)
        l1_delta = l1_error * nonlin(l1, deriv=True)

        # update weights
        weights3 += 0.15 * np.dot(l3.T, l4_delta)
        print(l3.T.shape)
        print(l4_delta.shape)
        weights2 += 0.15 * np.dot(l2.T, l3_delta)
        weights1 += 0.15 * np.dot(l1.T, l2_delta)
        weights0 += 0.15 * np.dot(l0.T, l1_delta)

        # if global error is small enough, stop
        if np.mean(np.abs(l4_error)) < 0.01:
            stop = True

        # replace this with separated train/test data scenario
        if j == 99999 or stop:
            l0 = X
            l1 = nonlin(np.dot(l0, weights0))
            l2 = nonlin(np.dot(l1, weights1))
            l3 = nonlin(np.dot(l2, weights2))
            l4 = nonlin(np.dot(l3, weights3))
            count = 0
            for i in range(len(y)):
                if abs(l4[i][0] - y[i][0]) < 0.15 and abs(l4[i][1] - y[i][1]) < 0.15:
                    print(str([round(elem, 4) for elem in l4[i]]) + " <> " + str(y[i]) + "HEEEEEEEYYA")
                    count += 1
                else:
                    print(str([round(elem, 4) for elem in l4[i]]) + " <> " + str(y[i]))
            print(str(count) + "/310")
        j += 1


def start():
    inData, outData = readData()

    # random.seed(420)
    # shuffle(inData)
    # random.seed(420)
    # shuffle(outData)
    #
    # network.learning(copy.deepcopy(inData[:250]), copy.deepcopy(outData[:250]))
    # network.testing(copy.deepcopy(inData[250:]), copy.deepcopy(outData[250:]))

def readData():
    inData = []
    outData = []
    """
    1 0 - Disk Hernia (DH)
    0 1 - Spondylolisthesis (SL)
    0 0 - Normal (NO)
    
    maybe try out: 
    1 0 0 - Disk Hernia (DH)
    0 1 0 - Spondylolisthesis (SL)
    0 0 1 - Normal (NO)
    """
    with open("column_3C.dat", "r") as file:
        for _ in range(310):
            r = file.readline().strip().split(" ")
            if r[6] == "DH":
                out = [1.0, 0.0]
            elif r[6] == "SL":
                out = [0.0, 1.0]
            else:
                out = [0.0, 0.0]
            outData.append(out)
            inData.append([float(r[0]),float(r[1]),float(r[2]),float(r[3]),float(r[4]),float(r[5])])
            #inData.append([nonlin(float(r[0])), nonlin(float(r[1])), nonlin(float(r[2])), nonlin(float(r[3])),nonlin(float(r[4])), nonlin(float(r[5]))])

    print(inData)
    # transform normalise to use nonlin
    normaliseData(inData)
    inData = [[nonlin(elem) for elem in row] for row in inData]
    print(inData)

    inData_np = np.array(inData)
    outData_np = np.array(outData)
    return inData_np, outData_np

def normaliseData(trainData, noExamples=310, noFeatures=6):
    # statistical normalisation
    # understand it and fancy it out a bit
    for j in range(noFeatures):
        summ = 0.0
        for i in range(noExamples):
            summ += trainData[i][j]
        mean = summ / noExamples
        squareSum = 0.0
        for i in range(noExamples):
            squareSum += (trainData[i][j] - mean) ** 2
        deviation = sqrt(squareSum / noExamples)
        for i in range(noExamples):
            trainData[i][j] = (trainData[i][j] - mean) / deviation


dostuff()

"""
TODO:
    parameterize:
        input layer neurons nr
        output layer neurons nr
        hidden layer neurons nr
        hidden layer count
        learning rate
        stop condition global error threshold
        stop condition nr epoch threshold
"""
"""
make a cycle which tries out everything and searches for best parameters
"""
