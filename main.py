from DataLoader import *
from Id3 import *
from InformationGain import *

trainData = DataLoader.LoadKaggle()
trainData.ReportDataTypes()

id3 = Id3()
id3.MaximumGainAttribute = InformationGain.EntropyMaximumGainAttribute
id3.Train(trainData)
print("Trained.")

