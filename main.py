from DataLoader import *
from Id3 import *
from InformationGain import *
from AdaBoost import *

trainData = DataLoader.LoadKaggleTrain()
#trainData.ReportDataTypes()
#print()
#trainData.ReportData(10)
#print()
testData = DataLoader.LoadKaggleTest(trainData)
#testData.ReportData(10)
#print()

#ID3 Algorithm
#id3 = Id3()
#id3.MaximumGainAttribute = InformationGain.EntropyMaximumGainAttribute
#id3.Train(trainData, 5)
#print("Training Error:", id3.Test(trainData))
#print()
#id3.PrintTree(3)
#predictions = id3.Predict(testData)

#AdaBoost Algorithm
ada = AdaBoost()
for i in range(250):
    ada.Train(trainData)
    trainE = ada.GetError(trainData)
    if i % 10 == 0:
        print("At iteration", i, "trainE:", trainE)
print("Train Error:", trainE)
predictions = ada.Predict(testData)

DataLoader.WritePredictions(testData, predictions)
print("Predictions.csv written.")



