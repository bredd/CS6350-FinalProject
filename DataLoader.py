from DataSet import *

# All methods are static
class DataLoader:

    def LoadKaggleTrain(limit=None, overrideCol=None, overrideVal=None):
        ds = DataSet()
        ds.Load("./Data/train_final.csv", 15, rowLimit=limit, hasTitleRow=True)
        ds.PartitionColumn(0, "Age", overrideVal if overrideCol == 0 else 7)
        ds.CategorizeColumn(1, "WorkClass", overrideVal if overrideCol == 1 else 0.01)
        ds.PartitionColumn(2, "Fnlwgt", overrideVal if overrideCol == 2 else 3) #fnlwgt
        ds.CategorizeColumn(3, "Education", overrideVal if overrideCol == 3 else 0.01)
        ds.RemoveColumn(4) #education.num
        ds.CategorizeColumn(4, "Marital", overrideVal if overrideCol == 4 else 0.01)
        ds.CategorizeColumn(5, "Occupation", overrideVal if overrideCol == 5 else 0.005)
        ds.CategorizeColumn(6, "Relationship", overrideVal if overrideCol == 6 else 0.05)
        ds.CategorizeColumn(7, "Race", overrideVal if overrideCol == 7 else 0.1)
        ds.CategorizeColumn(8, "Sex", overrideVal if overrideCol == 8 else 0.05)
        ds.CombineColumns(9, 10, lambda a, b: float(a)-float(b))
        ds.PartitionColumn(9, "CapitalGain", overrideVal if overrideCol == 9 else 3)
        ds.PartitionColumn(10, "HoursPerWeek", overrideVal if overrideCol == 10 else 7)
        ds.CategorizeColumn(11, "NativeCountry", overrideVal if overrideCol == 11 else 0.0075)
        ds.CategorizeColumn(12, "y", 0.05)
        return ds

    def LoadKaggleTest(dsTrain, limit=None):
        ds = DataSet()
        ds.Load("./Data/test_final.csv", 15, rowLimit=limit, hasTitleRow=True)
        ds.CopyColumn(0, 15)
        ds.RemoveColumn(0)
        ds.SetColumn(0, dsTrain.DataTypes[0]) #Age
        ds.SetColumn(1, dsTrain.DataTypes[1]) #WorkClass
        ds.SetColumn(2, dsTrain.DataTypes[2]) #Fnlwgt
        ds.SetColumn(3, dsTrain.DataTypes[3]) #Education
        ds.RemoveColumn(4) #education.num
        ds.SetColumn(4, dsTrain.DataTypes[4]) #Marital
        ds.SetColumn(5, dsTrain.DataTypes[5]) #Occupation
        ds.SetColumn(6, dsTrain.DataTypes[6]) #Relationship
        ds.SetColumn(7, dsTrain.DataTypes[7]) #Race
        ds.SetColumn(8, dsTrain.DataTypes[8]) #Sex
        ds.CombineColumns(9, 10, lambda a, b: float(a)-float(b))
        ds.SetColumn(9, dsTrain.DataTypes[9]) #CapitalGain
        ds.SetColumn(10, dsTrain.DataTypes[10]) #HoursPerWeek
        ds.SetColumn(11, dsTrain.DataTypes[11]) #NativeCountry
        ds.IntColumn(12, "ID")
        return ds

    def WritePredictions(dsTest, predictions, filename = "./predictions.csv"):
        ids = dsTest.Data[-1]
        with open (filename , 'w') as f:
            f.write("ID,Prediction\n")
            for i in range(len(ids)):
                f.write("%d,%d\n" % (ids[i], predictions[i]))

