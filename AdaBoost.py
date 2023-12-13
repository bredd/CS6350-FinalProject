import math

class AdaBoost:
    def __init__(self):
        self.D = None
        self.H = []
        self.Alphas = []

    def Train(self, dataSet):
        data = dataSet.Data
        colCount = len(data)
        rowCount = len(data[0])

        # 1. Initialize D
        if self.D is None:
            self.D = [1/rowCount for row in range(rowCount)]

        # One training instance
        stump = AdaBoost.GetStump(dataSet, self.D)
        self.H.append(stump)
        e = AdaBoost.__Error(dataSet, stump, self.D)
        #print("e:", e)
        alpha = math.log((1-e)/e)/2
        #print("alpha:", alpha)
        self.Alphas.append(alpha)

        #Update weights
        totalD = 0
        for i in range(rowCount):
            sign = -1 if stump.Classify(dataSet, i) == dataSet.Data[-1][i] else 1
            newD = self.D[i] * math.exp(alpha * sign)
            self.D[i] = newD
            totalD += newD
        for i in range(rowCount):
            self.D[i] /= totalD

    def GetError(self, dataSet):
        data = dataSet.Data
        colCount = len(data)
        rowCount = len(data[0])

        errCount = 0
        for i in range(rowCount):
            if self.__Classify(dataSet, i) != data[-1][i]:
                errCount += 1
        return errCount / rowCount

    def Predict(self, dataSet):
        data = dataSet.Data
        colCount = len(data)
        rowCount = len(data[0])

        predictions = []
        for i in range(rowCount):
            predictions.append(self.__Classify(dataSet, i))
        return predictions

    def GetStumpErrors(self, dataSet):
        Y = dataSet.Data[-1]
        rowCount = len(Y)

        errors = []
        for i in range(len(self.H)):
            errCount = 0
            for row in range(rowCount):
                if self.H[i].Classify(dataSet, row) != Y[row]:
                    errCount += 1
            errors.append(errCount/rowCount)
        return errors

    def __Classify(self, dataSet, row):
        sum = 0
        for i in range(len(self.H)):
            sum += self.Alphas[i] * (1 if self.H[i].Classify(dataSet, row) else -1)
        return sum >= 0

    class Stump:
        def __init__(self, attr, values):
            self.Attr = attr
            self.Values = values
        
        def Classify(self, dataSet, row):
            #print("Classify:", row, self.Values[dataSet.Data[self.Attr][row]])
            return self.Values[dataSet.Data[self.Attr][row]]

    @staticmethod
    def GetStump(dataSet, weights):
        attr = AdaBoost.EntropyMaximumGainAttribute(dataSet, weights)
        values = []
        for category in range(dataSet.DataTypes[attr].CategoryCount):
            values.append(AdaBoost.__MostWeightedValue(dataSet, attr, category, weights))
        return AdaBoost.Stump(attr, values)

    @staticmethod
    def EntropyMaximumGainAttribute(dataSet, weights):
        maxGain = -1
        bestAttribute = -1
        entropyOfS = AdaBoost.__Entropy(dataSet, weights)
        for attribute in range(len(dataSet.Data)-1):
            gain = entropyOfS - AdaBoost.__EntropyOfAttribute(dataSet, attribute, weights)
            if gain > maxGain:
                maxGain = gain
                bestAttribute = attribute
        return bestAttribute

    # This version requires a binary y and accepts weights
    # quite different from the version used by Id3
    @staticmethod
    def __Entropy(dataSet, weights):
        Y = dataSet.Data[-1]
        #weighted averages
        waTrue = 0
        for i in range(len(Y)):
            if Y[i]:
                waTrue += weights[i]
        if waTrue <= 0 or waTrue >= 1: return 0
        return -waTrue*math.log2(waTrue) - (1-waTrue)*math.log2(1-waTrue)

    # This version requires a binary y and accepts weights
    # quite different from the version used by Id3
    @staticmethod
    def __EntropyOfAttribute(dataSet, attribute, weights):
        #Initialization
        X = dataSet.Data[attribute]
        Y = dataSet.Data[-1]
        rowCount = len(Y)
        dt = dataSet.DataTypes[attribute]
        categoryCount = dt.CategoryCount
        counts = [0 for a in range(categoryCount)]
        waTrue = [0 for a in range(categoryCount)]
        waFalse = [0 for a in range(categoryCount)]

        #Get weighted average true for each attribute value
        for i in range(rowCount):
            counts[X[i]] += 1
            if Y[i]:
                waTrue[X[i]] += weights[i]
            else:
                waFalse[X[i]] += weights[i]

        #Sum up the weighted entropy
        entropy = 0
        entropy2 = 0
        for i in range(categoryCount):
            twa = waTrue[i]/(waTrue[i]+waFalse[i])
            if twa == 0: twa = 0.00001/waFalse[i]
            entropy += counts[i]/rowCount * (-twa*math.log2(twa) - (1-twa)*math.log2(1-twa))
        return entropy

    @staticmethod
    def __MostWeightedValue(dataSet, attribute, category, weights):
        X = dataSet.Data[attribute]
        Y = dataSet.Data[-1]
        wTrue = 0
        wFalse = 0
        for i in range(len(Y)):
            if X[i] == category:
                if Y[i]:
                    wTrue += weights[i]
                else:
                    wFalse += weights[i]
        return 1 if wTrue >= wFalse else 0

    @staticmethod
    def __Error(dataSet, stump, weights):
        X = dataSet.Data[stump.Attr]
        Y = dataSet.Data[-1]
        v = stump.Values
        sum = 0
        for i in range(len(X)):
            if v[X[i]] != Y[i]:
                sum += weights[i]
        return sum
