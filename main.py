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
Iterations=280
ada = AdaBoost()
bestIterations = 0
bestError = 1.0
for i in range(Iterations):
    ada.Train(trainData)
    trainE = ada.GetError(trainData)
    if bestError > trainE:
        bestError = trainE
        bestIterations = i
        print("At iteration", i, "trainE:", trainE)
print("After %d iterations:" % Iterations)
print("Train Error:", trainE)
predictions = ada.Predict(testData)

DataLoader.WritePredictions(testData, predictions)
print("Predictions.csv written.")



