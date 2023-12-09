from DataLoader import *
from Id3 import *
from InformationGain import *

trainData = DataLoader.LoadKaggleTrain()
#trainData.ReportDataTypes()
#print()
#trainData.ReportData(10)
#print()
testData = DataLoader.LoadKaggleTest(trainData)
#testData.ReportData(10)
#print()

id3 = Id3()
id3.MaximumGainAttribute = InformationGain.EntropyMaximumGainAttribute
id3.Train(trainData, 8)
print("Training Error:", id3.Test(trainData))
print()
#id3.PrintTree(3)

predictions = id3.Predict(testData)
DataLoader.WritePredictions(testData, predictions)
print("Predictions.csv written.")



