class DataType:
    def __init__(self, name, categories = None, partitionPoints = None):
        self.Name = name
        self.Categories = categories
        self.DivisionPoints = partitionPoints

class DataSet:
    def Load(self, filename, colCount, rowLimit=None, hasTitleRow=False):
        if rowLimit is None:
            rowLimit = 1000000
        data = [[] for i in range(colCount)]
        with open (filename , 'r') as f:
            count = 0
            skip = not hasTitleRow
            for line in f:
                if skip:
                    skip = False
                    continue
                if count >= rowlimit: break
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

    def CategorizeColumn(self, colNum, name, categories):
        for i in range(len(self.Data[colNum])):
            try:
                data[colNum][i] = categories.index(data[colNum][i]))
            except ValueError:
                print("Value ", data[colNum][i], " not found in DataType ", name, i)
                raise
        self.DataTypes[colNum] = new DataType(name, categories)

    def ContinuousColumn(self, colNum, name):
        DataSet.FloatData(self.Data[colNum])
        self.DataTypes[colNum] = new DataType(name)

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
            else arrayIndex < len(colData)-1:
                partitionPoints[i] = colData[arrayIndex]*(1-arrayFraction) + colData[arrayIndex+1]*arrayFraction
        partitionPoints[partitionCount-1] = float('inf') # Infinity
        partitionData(colData)
        self.DataTypes[colNum] = new DataType(name, partitionPoints = partitionPoints)

    def SetColumn(self, colNum, dataType):
        if dataType.Categories is not None:
            self.CategorizeColumn(colNum, dataType.Name, dataType.Categories)
        elif dataType.PartitionPoints is not None:
            DataSet.FloatData(self.Data[colNum])
            DataSet.PartitionData(self.Data[colNum], dataType.PartitionPoints)
            self.DataTypes[colNum] = new DataType(name, partitionPoints = dataType.PartitionPoints)
        else
            self.ContinuousColumn(colNum, dataType.Name)

    def BinaryToSigned(self, colNum):
        col = self.Data[colNum]
        for i in range(len(col)):
            col[i] = 1 if col[i] > 0 else -1

    @staticmethod
    def PartitionData(data, partitionPoints):
        for i in range(len(data)):
            datum = data[i]
            for j in range(partitionPoints):
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

    def Dump(self):
        colCount = len(self.Data)
        rowCount = len(self.Data[0])
        for dt in self.DataTypes:
            print(dt.Name, end="\t")
        print()
        for row in range(0,rowCount):
            for col in range(0,colCount):
                dt = self.DataTypes[col]
                if dt.Categories is None:
                    print(self.Data[col][row], end="\t")
                else:
                    print(dt.Categories[self.Data[col][row]])
            print()
        print(rowCount, "Rows")
