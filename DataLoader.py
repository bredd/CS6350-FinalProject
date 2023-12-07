from DataSet import *
from collections import Counter
import statistics

# All methods are static
class DataLoader:

    def LoadKaggle(limit=None):
        ds = DataSet()
        ds.Load("./Data/train_final.csv", 15, rowLimit=limit, hasTitleRow=True)
        ds.PartitionColumn(0, "Age", 6)
        ds.CategorizeColumn(1, "WorkClass", ("Private", "Federal-gov", "Local-gov", "State-gov", "Self-emp-inc", "Self-emp-not-inc", "Without-pay", "Never-worked", "?"))
        ds.RemoveColumn(2) #fnlwgt
        ds.CategorizeColumn(2, "Education", ("Preschool", "1st-4th", "5th-6th", "7th-8th", "9th", "10th", "11th", "12th", "HS-grad", "Some-college", "Assoc-voc", "Assoc-acdm", "Bachelors", "Masters", "Prof-school", "Doctorate"))
        ds.RemoveColumn(3) #education.num
        ds.CategorizeColumn(3, "Marital", ("Never-married", "Married-civ-spouse", "Married-AF-spouse", "Married-spouse-absent", "Widowed", "Separated", "Divorced"))
        ds.CategorizeColumn(4, "Occupation", ("Adm-clerical", "Armed-Forces", "Craft-repair", "Exec-managerial", "Farming-fishing", "Handlers-cleaners", "Machine-op-inspct", "Other-service", "Priv-house-serv", "Prof-specialty", "Protective-serv", "Sales", "Tech-support", "Transport-moving", "?"))
        ds.CategorizeColumn(5, "Relationship", ("Wife", "Husband", "Unmarried", "Own-child", "Other-relative", "Not-in-family"))
        ds.CategorizeColumn(6, "Race", ("White", "Black", "Amer-Indian-Eskimo", "Asian-Pac-Islander", "Other"))
        ds.CategorizeColumn(7, "Sex", ("Female", "Male"))
        ds.PartitionColumn(8, "CapitalGain", 3)
        ds.PartitionColumn(9, "HoursPerWeek", 5)
        ds.CategorizeColumn(10, "NativeCountry", ())
        ds.CategorizeColumn(11, "y", ("0", "1"))

# Detect categories rather than make them explicit
# Categorize unknown as most-common
# Lump less-common values together
