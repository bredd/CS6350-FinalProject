from collections import Counter
from collections import defaultdict
import random

class DataType:
    def __init__(self, name):
        self.Name = name
        self.CategoryCount=0
        self.PartitionPoints = None
        self.ValueMap = None
        self.ReverseMap = None

    def ValToString(self, value):
        if self.ReverseMap is not None:
            return self.ReverseMap[value]
        if self.PartitionPoints is not None:
            return "<%g" % (self.PartitionPoints[value])
        return str(value)

class DataSet:
    def Load(self, filename, colCount, rowLimit=None, hasTitleRow=False):
        if rowLimit is None:
            rowLimit = 1000000
        data = [[] for i in range(colCount)]
        with open (filename , 'r') as f:
            count = 0
            skip = hasTitleRow
            for line in f:
                if skip:
                    skip = False
                    continue
                if count >= rowLimit: break
                count += 1
                
                terms = line.strip().split(',')
                col = 0
                for col in range(colCount):
                    data[col].append(terms[col])
        self.Data = data
        self.DataTypes = [None for i in range(colCount)]

    # The following functions prepare each column
    def RemoveColumn(self, colNum):
        self.Data.pop(colNum)
        self.DataTypes.pop(colNum)

    def CategorizeColumn(self, colNum, name, threshold):
        rowCount = len(self.Data[colNum])

        # Find and count the distinct values
        counter = Counter(self.Data[colNum])

        # Create a map of values to indices in order of frequency
        # All values below the threshold get the same index
        # Also create the reverse map
        map={}
        reverseMap=[]
        index=0
        hasOther = False
        mostCommon = counter.most_common()
        for pair in mostCommon:
            if pair[0] == "?":
                map["?"] = 0 # Replace unknown with the most common which is index 0
            elif pair[0] == "Other":
                hasOther = True
            else:
                map[pair[0]] = index
                # All counts below the fraction threshold get the "Other" index
                if pair[1] / rowCount >= threshold:
                    reverseMap.append(pair[0])
                    index += 1
                else:
                    hasOther = True
        
        if hasOther:
            map["Other"] = index
            reverseMap.append("Other")
            index += 1

        # Now that maps have been created, map the data
        DataSet.MapData(self.Data[colNum], map, len(reverseMap)-1)

        # Add the DataType
        dt = DataType(name)
        dt.CategoryCount = len(reverseMap)
        dt.ValueMap = map
        dt.ReverseMap = reverseMap
        dt.MostCommon = mostCommon
        self.DataTypes[colNum] = dt

    def ContinuousColumn(self, colNum, name):
        DataSet.FloatData(self.Data[colNum])
        self.DataTypes[colNum] = DataType(name)

    def IntColumn(self, colNum, name):
        DataSet.IntData(self.Data[colNum])
        self.DataTypes[colNum] = DataType(name)

    def PartitionColumn(self, colNum, name, partitionCount):
        DataSet.FloatData(self.Data[colNum]) # Convert to float
        colData = self.Data[colNum].copy() # Make a copy of the data
        colData.sort() # Sort into ascending order
        partitionPoints = []
        partitionCounts = []
        targetCount = len(colData)/partitionCount

        # Find the partition points
        partitionCount=0
        partitionPoint=0
        value=0
        valueI=0
        valueCount=0
        for i in range(len(colData)):
            v = colData[i]
            if v != value:
                if (valueCount >= targetCount or partitionCount+targetCount >= targetCount * 1.5) and partitionCount > 0:
                    # Value can make its own partition so save the preceding partition
                    partitionPoints.append(colData[valueI] if valueI==0 else (float(colData[valueI-1])+colData[valueI])/2)
                    #if valueI>0: print("A", colData[valueI-1], colData[valueI], colData[valueI] if valueI==0 else (colData[valueI-1]+colData[valueI])/2)
                    partitionCounts.append(partitionCount)
                    partitionCount = 0
                if partitionCount + valueCount >= targetCount:
                    # Save this partition
                    partitionPoints.append(v if i==0 else (colData[i-1]+colData[i])/2)
                    #if i>0: print("B", colData[i-1], colData[i])
                    partitionCounts.append(partitionCount+valueCount)
                    partitionCount = 0
                else:
                    partitionCount += valueCount
                valueCount = 0
                value = v
                valueI = i
            valueCount += 1
        partitionPoints.append(float('inf'))
        partitionCounts.append(partitionCount+valueCount)
        DataSet.PartitionData(self.Data[colNum], partitionPoints)

        # Add the DataType
        dt = DataType(name)
        dt.CategoryCount = len(partitionPoints)
        dt.PartitionPoints = partitionPoints
        dt.PartitionCounts = partitionCounts
        self.DataTypes[colNum] = dt

    def CombineColumns(self, colA, colB, cfunc):
        data = self.Data
        for i in range(len(data[colA])):
            data[colA][i] = cfunc(data[colA][i], data[colB][i])
        self.RemoveColumn(colB)


    def CopyColumn(self, src, dst):
        self.Data.insert(dst, self.Data[src])
        self.DataTypes.insert(dst, self.DataTypes[src])

    def SetColumn(self, colNum, dataType):
        if dataType.ValueMap is not None:
            DataSet.MapData(self.Data[colNum], dataType.ValueMap, len(dataType.ReverseMap)-1)
        elif dataType.PartitionPoints is not None:
            DataSet.FloatData(self.Data[colNum])
            DataSet.PartitionData(self.Data[colNum], dataType.PartitionPoints)
        else:
            DataSet.FloatData(self.Data[colNum])
        self.DataTypes[colNum] = dataType

    def BinaryToSigned(self, colNum):
        col = self.Data[colNum]
        for i in range(len(col)):
            col[i] = 1 if col[i] > 0 else -1

    def Split(self, rSeed):
        random.seed(rSeed)
        data=self.Data
        colCount=len(data)
        rowCount=len(data[0])
        dataOut = []
        dataOut.append([[] for j in range(colCount)])
        dataOut.append([[] for j in range(colCount)])
        for i in range(rowCount):
            r = random.randint(0,1)
            for j in range(colCount):
                dataOut[r][j].append(data[j][i])
        ds0 = DataSet()
        ds0.DataTypes = self.DataTypes
        ds0.Data = dataOut[0]
        ds1 = DataSet()
        ds1.DataTypes = self.DataTypes
        ds1.Data = dataOut[1]
        return (ds0, ds1)

    @staticmethod
    def MapData(data, map, otherValue):
        for i in range(len(data)):
            mappedValue = map.get(data[i])
            if mappedValue is None:
                #print("Unexpected value:", data[i])
                mappedValue = otherValue
            data[i] = mappedValue

    @staticmethod
    def PartitionData(data, partitionPoints):
        pointCount = len(partitionPoints)
        for i in range(len(data)):
            datum = data[i]
            for j in range(pointCount):
                if datum < partitionPoints[j]:
                    data[i] = j
                    break

    @staticmethod
    def FloatData(data):
        for i in range(len(data)):
            try:
                data[i] = float(data[i])
            except:
                print("Value", data[i], "is not numeric.")
                raise

    @staticmethod
    def IntData(data):
        for i in range(len(data)):
            try:
                data[i] = int(data[i])
            except:
                print("Value", data[i], "is not an integer.")
                raise

    def ReportDataTypes(self):
        for i in range(len(self.DataTypes)):
            dt = self.DataTypes[i]
            if dt.ValueMap is not None:
                print("%d %s: Categorized" % (i, dt.Name))
                rowCount = len(self.Data[i])
                mostCommonMap = defaultdict(int)
                for pair in dt.MostCommon:
                    mostCommonMap[pair[0]] = pair[1] / rowCount
                for i in range(len(dt.ReverseMap)):
                    print("  %d %s:" % (i, dt.ReverseMap[i]), end="")
                    for pair in dt.ValueMap.items():
                        if pair[1] == i:
                            print(" %s(%.3f)" % (pair[0], mostCommonMap[pair[0]]), end="")
                    print()
            elif dt.PartitionPoints is not None:
                print("%d %s: Partitioned" % (i, dt.Name))
                rowCount = len(self.Data[i])
                print("  (%.3f)" % (dt.PartitionCounts[0]/rowCount), end="")
                for i in range(len(dt.PartitionPoints)-1):
                    print(" %g (%.3f)" % (dt.PartitionPoints[i], dt.PartitionCounts[i+1]/rowCount), end="")
                print()
            else:
                print("%d %s: Continuous" % (i, dt.Name))

    def ReportData(self, maxRows):
        colCount = len(self.Data)
        rowCount = min(len(self.Data[0]), maxRows)
        for dt in self.DataTypes:
            print(dt.Name, end="\t")
        print()
        for row in range(0,rowCount):
            for col in range(0,colCount):
                dt = self.DataTypes[col]
                if dt.ReverseMap is None:
                    print(self.Data[col][row], end="\t")
                else:
                    print(dt.ReverseMap[self.Data[col][row]], end="\t")
            print()
        print(rowCount, "Rows")
