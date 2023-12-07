from collections import Counter
from collections import defaultdict

class DataType:
    def __init__(self, name):
        self.Name = name
        self.PartitionPoints = None
        self.ValueMap = None
        self.ReverseMap = None

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
        DataSet.MapData(self.Data[colNum], map)

        # Add the DataType
        dt = DataType(name)
        dt.ValueMap = map
        dt.ReverseMap = reverseMap
        dt.MostCommon = mostCommon
        self.DataTypes[colNum] = dt

    def ContinuousColumn(self, colNum, name):
        DataSet.FloatData(self.Data[colNum])
        self.DataTypes[colNum] = DataType(name)

    def PartitionColumn(self, colNum, name, partitionCount):
        DataSet.FloatData(self.Data[colNum]) # Convert to float
        colData = self.Data[colNum].copy() # Make a copy of the data
        colData.sort() # Sort into ascending order
        partitionPoints = [0 for i in range(partitionCount)]

        # Find the partition points
        for i in range(partitionCount-1):
            arrayPoint = (len(colData)/partitionCount)*i
            arrayIndex = int(arrayPoint)
            arrayFraction = arrayPoint-arrayIndex
            if arrayFraction == 0 or arrayIndex >= len(colData)-1:
                partitionPoints[i] = colData[arrayIndex]
            else:
                partitionPoints[i] = colData[arrayIndex]*(1-arrayFraction) + colData[arrayIndex+1]*arrayFraction
        partitionPoints[partitionCount-1] = float('inf') # Infinity
        DataSet.PartitionData(colData, partitionPoints)

        # Add the DataType
        dt = DataType(name)
        dt.PartitionPoints = partitionPoints
        self.DataTypes[colNum] = dt

    def SetColumn(self, colNum, dataType):
        if dataType.ValueMap is not None:
            DataSet.MapData(self.Data[colNum], dataType.ValueMap)
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

    @staticmethod
    def MapData(data, map):
        for i in range(len(data)):
            mappedValue = map[data[i]]
            if mappedValue is None:
                print("Unexpected value:", data[i])
                raise ValueError("Unexpected value: " + data[i])
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
                print(" ", end="")
                for point in dt.PartitionPoints:
                    print("", point, end="")
                print()
            else:
                print("%d %s: Continuous" % (i, dt.Name))

    def ReportData(self):
        colCount = len(self.Data)
        rowCount = len(self.Data[0])
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
