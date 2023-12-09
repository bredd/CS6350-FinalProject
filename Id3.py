from DataSet import *
from Trace import *
from collections import Counter

class Id3:

    class Node:
        def Evaluate(self, args):
            raise NotImplemented("Evaluate is an abstract method.")

        def Print(self, level, dataTypes):
            raise NotImplemented("Print is an abstract method.")

    class LeafNode(Node):
        def __init__(self, label):
            self.Label = label

        def Evaluate(self, args):
            return self.Label

        def Print(self, level, dataTypes, maxDepth):
            dt = dataTypes[-1]
            print(level*"   ", dt.Name, "=", self.Label, sep="")

    class MidNode(Node):
        def __init__(self, attr, childNodes):
            self.Attr = attr
            self.ChildNodes = childNodes

        def Evaluate(self, args):
            return self.ChildNodes[args[self.Attr]].Evaluate(args)

        def Print(self, level, dataTypes, maxDepth):
            if level >= maxDepth: return
            dt = dataTypes[self.Attr]
            for i in range(0, len(self.ChildNodes)):
                print(level*"   ", dt.Name, "=", dt.ValToString(i), sep="")
                self.ChildNodes[i].Print(level+1, dataTypes, maxDepth)

    def Train(self, dataSet, maxDepth = 10000):
        attributes = list(range(0,len(dataSet.DataTypes)-1))
        self.DataTypes = dataSet.DataTypes
        self.Tree = self.__Id3(dataSet.Data, attributes, maxDepth)

    def __Id3(self, S, attributes, maxDepth):
        labelIndex = len(S)-1

        # Exit if all labels in S are the same
        if Id3.__haveSameValue(S[labelIndex]):
            return Id3.LeafNode(S[labelIndex][0])

        # Exit if there are no more attributes to evaluate or if we've reached the maximum depth
        if len(attributes) == 0 or maxDepth == 0:
            return Id3.LeafNode(Id3.__mostCommonValue(S[labelIndex]))
        
        # This will be one of the three information gain algorithms
        attr = self.MaximumGainAttribute(S, attributes, self.DataTypes)

        # Split recursively
        childNodes = []
        subAttributes = list(attributes) # duplicate the list
        subAttributes.remove(attr)
        for catIndex in range(0, self.DataTypes[attr].CategoryCount):
            subset = Id3.__select(S, attr, catIndex)
            if len(subset[0]) == 0:
                childNodes.append(Id3.LeafNode(Id3.__mostCommonValue(S[labelIndex])))
            else:
                childNodes.append(self.__Id3(subset, subAttributes, maxDepth-1))
        return Id3.MidNode(attr, childNodes)

    def PrintTree(self, maxDepth):
        self.Tree.Print(0, self.DataTypes, maxDepth)

    def Test(self, dataSet):
        S = dataSet.Data
        labelIndex = len(S)-1
        count = len(S[0])
        errors = 0
        for i in range(0, count):
            row = Id3.__getRow(S, i)
            label = self.Tree.Evaluate(row)
            if label != row[labelIndex]:
                if Trace.Verbosity > 1:
                    print(self.DataTypes[labelIndex].Categories[label], "!=", self.DataTypes[labelIndex].Categories[row[labelIndex]])
                errors += 1
        return errors / count

    def Predict(self, dataSet):
        S = dataSet.Data
        predictions = []
        for i in range(0, len(S[0])):
            predictions.append(self.Tree.Evaluate(Id3.__getRow(S, i)))
        return predictions

    @staticmethod
    def __haveSameValue(a):
        firstVal = a[0]
        for v in a:
            if v != firstVal:
                return False
        return True

    @staticmethod
    def __mostCommonValue(a):
        ctr = Counter(a)
        return ctr.most_common(1)[0][0]

    @staticmethod
    def __select(S, attr, catIndex):
        # This is probably not the most efficient but I'm not yet a Python expert
        result = []
        for i in range(0, len(S)):
            result.append([])
        for i in range(0, len(S[0])):
            if S[attr][i] == catIndex:
                for j in range(0, len(S)):
                    result[j].append(S[j][i])
        return result

    @staticmethod
    def __getRow(S, index):
        # A python expert might have a more efficient method for this
        row = []
        for i in range(0, len(S)):
            row.append(S[i][index])
        return row
    
        