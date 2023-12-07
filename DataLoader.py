from DataSet import *

# All methods are static
class DataLoader:

    def LoadKaggle(limit=None):
        ds = DataSet()
        ds.Load("./Data/train_final.csv", 15, rowLimit=limit, hasTitleRow=True)
        ds.PartitionColumn(0, "Age", 6)
        ds.CategorizeColumn(1, "WorkClass", 0.05)
        ds.RemoveColumn(2) #fnlwgt
        ds.CategorizeColumn(2, "Education", 0.01)
        ds.RemoveColumn(3) #education.num
        ds.CategorizeColumn(3, "Marital", 0.05)
        ds.CategorizeColumn(4, "Occupation", 0.05)
        ds.CategorizeColumn(5, "Relationship", 0.05)
        ds.CategorizeColumn(6, "Race", 0.05)
        ds.CategorizeColumn(7, "Sex", 0.05)
        ds.PartitionColumn(8, "CapitalGain", 3)
        ds.PartitionColumn(9, "CapitalLoss", 3)
        ds.PartitionColumn(10, "HoursPerWeek", 5)
        ds.CategorizeColumn(11, "NativeCountry", 0.05)
        ds.CategorizeColumn(12, "y", 0.05)
        return ds
