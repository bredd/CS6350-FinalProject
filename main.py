from DataLoader import *
from Id3 import *
from InformationGain import *

trainData = DataLoader.LoadKaggle()
trainData.ReportDataTypes()
print()
trainData.ReportData(10)
print()

id3 = Id3()
id3.MaximumGainAttribute = InformationGain.EntropyMaximumGainAttribute
id3.Train(trainData)
print("Trained.")
print("Training Error:", id3.Test(trainData))

