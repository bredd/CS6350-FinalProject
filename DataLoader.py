from DataSet import *

# All methods are static
class DataLoader:

    def LoadKaggleTrain(limit=None):
        ds = DataSet()
        ds.Load("./Data/train_final.csv", 15, rowLimit=limit, hasTitleRow=True)
        ds.PartitionColumn(0, "Age", 10)
        ds.CategorizeColumn(1, "WorkClass", 0.05)
        ds.RemoveColumn(2) #fnlwgt
        ds.CategorizeColumn(2, "Education", 0.01)
        ds.RemoveColumn(3) #education.num
        ds.CategorizeColumn(3, "Marital", 0.05)
        ds.CategorizeColumn(4, "Occupation", 0.05)
        ds.CategorizeColumn(5, "Relationship", 0.05)
        ds.CategorizeColumn(6, "Race", 0.05)
        ds.CategorizeColumn(7, "Sex", 0.05)
        ds.CombineColumns(8, 9, lambda a, b: float(a)-float(b))
        ds.PartitionColumn(8, "CapitalGain", 3)
        ds.PartitionColumn(9, "HoursPerWeek", 8)
        ds.CategorizeColumn(10, "NativeCountry", 0.001)
        ds.CategorizeColumn(11, "y", 0.05)
        return ds

    def LoadKaggleTest(dsTrain, limit=None):
        ds = DataSet()
        ds.Load("./Data/test_final.csv", 15, rowLimit=limit, hasTitleRow=True)
        ds.CopyColumn(0, 15)
        ds.RemoveColumn(0)
        ds.SetColumn(0, dsTrain.DataTypes[0]) #Age
        ds.SetColumn(1, dsTrain.DataTypes[1]) #WorkClass
        ds.RemoveColumn(2) #fnlwgt
        ds.SetColumn(2, dsTrain.DataTypes[2]) #Education
        ds.RemoveColumn(3) #education.num
        ds.SetColumn(3, dsTrain.DataTypes[3]) #Marital
        ds.SetColumn(4, dsTrain.DataTypes[4]) #Occupation
        ds.SetColumn(5, dsTrain.DataTypes[5]) #Relationship
        ds.SetColumn(6, dsTrain.DataTypes[6]) #Race
        ds.SetColumn(7, dsTrain.DataTypes[7]) #Sex
        ds.CombineColumns(8, 9, lambda a, b: float(a)-float(b))
        ds.SetColumn(8, dsTrain.DataTypes[8]) #CapitalGain
        ds.SetColumn(9, dsTrain.DataTypes[9]) #HoursPerWeek
        ds.SetColumn(10, dsTrain.DataTypes[10]) #NativeCountry
        ds.IntColumn(11, "ID")
        return ds

    def WritePredictions(dsTest, predictions, filename = "./predictions.csv"):
        ids = dsTest.Data[-1]
        with open (filename , 'w') as f:
            f.write("ID,Prediction\n")
            for i in range(len(ids)):
                f.write("%d,%d\n" % (ids[i], predictions[i]))

