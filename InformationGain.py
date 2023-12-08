from collections import Counter
import math
from Trace import *

# Static class
class InformationGain:

    # Static variable controlling rounding
    RoundGain = False

    @staticmethod
    def TrivialMaximumGainAttribute(S, attributes, dataTypes):
        return attributes[0]

    @staticmethod
    def EntropyMaximumGainAttribute(S, attributes, dataTypes):
        if Trace.Verbosity > 0:
            print("EntropyMaximumGain")
        maxGain = -1
        bestAttribute = -1
        entropyOfS = InformationGain.__Entropy(S)
        for attribute in attributes:
            gain = entropyOfS - InformationGain.__EntropyOfAttribute(S, attribute, dataTypes)
            if Trace.Verbosity > 0:
                print("  Gain", dataTypes[attribute].Name, "=", gain)
            if gain > maxGain:
                maxGain = gain
                bestAttribute = attribute
        return bestAttribute

    @staticmethod
    def __Entropy(S):
        ctr = Counter(S[len(S)-1])
        sum = 0
        tot = ctr.total()
        for c in ctr.values():
            p = c/tot
            sum -= p*math.log2(p)
        return sum

    @staticmethod
    def __EntropyOfAttribute(S, attribute, dataTypes):
        dt = dataTypes[attribute]
        sum = 0
        for value in range(0, dt.CategoryCount):
            sum += InformationGain.__EntropyWhere(S, attribute, value)
        return sum

    @staticmethod
    def __EntropyWhere(S, attribute, attrValue):
        attrs = S[attribute]
        labels = S[len(S)-1]
        ctr = Counter()
        for i in range(0, len(attrs)):
            if attrs[i] == attrValue:
                ctr.update((labels[i],))
        sum = 0
        tot = ctr.total()
        for c in ctr.values():
            p = c/tot
            sum -= p*math.log2(p)
        return (tot/len(attrs))*sum #weighted value

    @staticmethod
    def MajorityErrorMaximumGainAttribute(S, attributes, dataTypes):
        if Trace.Verbosity > 0:
            print("MajorityErrorMaximumGain")
        maxGain = -1
        bestAttribute = -1
        meOfS = InformationGain.__MajorityError(S)
        for attribute in attributes:
            gain = meOfS - InformationGain.__MajorityErrorOfAttribute(S, attribute, dataTypes)
            if InformationGain.RoundGain:
                gain = round(gain, 4)
            if Trace.Verbosity > 0:
                print("  Gain", dataTypes[attribute].Name, "=", gain)
            if gain > maxGain:
                maxGain = gain
                bestAttribute = attribute
        return bestAttribute

    @staticmethod
    def __MajorityError(S):
        ctr = Counter(S[len(S)-1])
        majorityCount = ctr.most_common(1)[0][1]
        tot = ctr.total()
        return (tot-majorityCount)/tot

    @staticmethod
    def __MajorityErrorOfAttribute(S, attribute, dataTypes):
        dt = dataTypes[attribute]
        sum = 0
        for value in range(0, len(dt.Categories)):
            sum += InformationGain.__MajorityErrorWhere(S, attribute, value)
        return sum

    @staticmethod
    def __MajorityErrorWhere(S, attribute, attrValue):
        attrs = S[attribute]
        labels = S[len(S)-1]
        ctr = Counter()
        for i in range(0, len(attrs)):
            if attrs[i] == attrValue:
                ctr.update((labels[i],))
        tot = ctr.total()
        if tot == 0:
            return 0
        majorityCount = ctr.most_common(1)[0][1]
        return (tot/len(attrs))*((tot-majorityCount)/tot)
        
    @staticmethod
    def GiniMaximumGainAttribute(S, attributes, dataTypes):
        if Trace.Verbosity > 0:
            print("GiniMaximumGain")
        maxGain = -1
        bestAttribute = -1
        meOfS = InformationGain.__Gini(S)
        for attribute in attributes:
            gain = meOfS - InformationGain.__GiniOfAttribute(S, attribute, dataTypes)
            if InformationGain.RoundGain:
                gain = round(gain, 4)
            if Trace.Verbosity > 0:
                print("  Gain", dataTypes[attribute].Name, "=", gain)
            if gain > maxGain:
                maxGain = gain
                bestAttribute = attribute
        return bestAttribute

    @staticmethod
    def __Gini(S):
        ctr = Counter(S[len(S)-1])
        tot = ctr.total()
        sum = 0
        for c in ctr.values():
            sum += (c/tot)**2
        return 1-sum

    @staticmethod
    def __GiniOfAttribute(S, attribute, dataTypes):
        dt = dataTypes[attribute]
        sum = 0
        for value in range(0, len(dt.Categories)):
            sum += InformationGain.__GiniWhere(S, attribute, value)
        return sum

    @staticmethod
    def __GiniWhere(S, attribute, attrValue):
        attrs = S[attribute]
        labels = S[len(S)-1]
        ctr = Counter()
        for i in range(0, len(attrs)):
            if attrs[i] == attrValue:
                ctr.update((labels[i],))
        tot = ctr.total()
        if tot == 0:
            return 0
        sum = 0
        for c in ctr.values():
            sum += (c/tot)**2
        return (tot/len(attrs))*(1-sum)
        