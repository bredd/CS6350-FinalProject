from DataLoader import *
from Id3 import *
from InformationGain import *
from AdaBoost import *

# Use Cross-Validation to optimize a parameter

# Optimize Hours Partition Count
Column = 9
Range = range(8, 14)
TrainingIterations = 250

bestErr = 1
bestArg = 0
for arg in Range:
    print("-----")
    dsAll = DataLoader.LoadKaggleTrain(overrideCol=Column, overrideVal=arg)

    sumErr = 0
    for split in range(0, 4):
        (dsTrain, dsTest) = dsAll.Split(split*25) # Use fixed seed for deterministic results
        ada = AdaBoost()
        for i in range(TrainingIterations):
            ada.Train(dsTrain)
            print('.', end='', flush=True)
        print()
        testErr = ada.GetError(dsTest)
        print("TestErr:", testErr)
        sumErr += testErr

    avgErr = sumErr/4
    print("Arg:", arg, "Err", avgErr)
    if (bestErr > avgErr):
        bestErr = avgErr
        bestArg = arg

print("Best arg for column %d is %g" % (Column, bestArg))
