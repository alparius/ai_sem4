"""
TODO
    2. Establish if a patient suffers of disk hernia, spondilose or if is healthy based on the information collected
    from other patients (regarding the shape and the orientation of the pelvis and the lumbar section of the spine).

TODO
    Each patient is represented in the data set by six biomechanical attributes derived from the shape and orientation
    of the pelvis and lumbar spine (in this order): pelvic incidence,
                                                    pelvic tilt,
                                                    lumbar lordosis angle,
                                                    sacral slope,
                                                    pelvic radius and
                                                    grade of spondylolisthesis.
    The following convention is used for the class labels: Disk Hernia (DH),
                                                           Spondylolisthesis (SL) and
                                                           Normal (NO).
"""
import copy
from math import sqrt, exp
from random import shuffle
import random

from Network import Network

"""
    Available tools that implements learning methods:
        1. Weka http://www.cs.waikato.ac.nz/ml/weka/
        2. Matlab http://www.mathworks.com/products/neural-network/
        3. OpenCV http://docs.opencv.org/modules/ml/doc/neural_networks.html
        4. Scikit http://scikit-learn.org/stable/
        5. GPLAB http://gplab.sourceforge.net/
        6. ECJ http://cs.gmu.edu/~eclab/projects/ecj/
"""

#sigmoid and its derivative
def sigmoid(x):
    return 1/(1+exp(-x))

def sigmoid_deriv(x):
    return sigmoid(x)*(1 - sigmoid(x))

class Application:
    def __init__(self):
        # normaliseData(noTrainExamples, noFeatures, inTrainData, noTestExamples, inTestData)
        self.network = Network(noInputs=6, noOutputs=3, noHiddenLayers=2, noNeuronsPerHiddenLayer=4)

    def start(self):
        inData, outData = self.readData()

        random.seed(420)
        shuffle(inData)
        random.seed(420)
        shuffle(outData)

        self.network.learning(copy.deepcopy(inData[:250]), copy.deepcopy(outData[:250]))
        self.network.testing(copy.deepcopy(inData[250:]), copy.deepcopy(outData[250:]))

    def readData(self):
        inData = []
        outData = []
        with open("column_3C.dat", "r") as file:
            for _ in range(310):
                r = file.readline().strip().split(" ")
                if r[6] == "DH":
                    out = [1, 0, 0]
                elif r[6] == "SL":
                    out = [0, 1, 0]
                else:
                    out = [0, 0, 1]
                outData.append(out)
                inData.append([float(r[0]),float(r[1]),float(r[2]),float(r[3]),float(r[4]),float(r[5])])
        return inData, outData


    def normaliseData(self, noExamples, noFeatures, trainData, noTestExamples, testData):
        # statistical normalisation
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
            for i in range(noTestExamples):
                testData[i][j] = (testData[i][j] - mean) / deviation
        # min-max normalization
        """
        for j in range(noFeatures):
            minn=min([trainData[i][j] for i in range(noExamples)])
            maxx=max([trainData[i][j] for i in range(noExamples)])
            for i in range(noExamples):
                trainData[i][j]=LIM_MIN+trainData[i][j]*(LIM_MAX-LIM_MIN)/(maxx - minn)
             for i in range(noTestExamples):
                testData[i][j]=LIM_MIN+testData[i][j]*(LIM_MAX-LIM_MIN)/(maxx - minn)
        """


a = Application()
a.start()