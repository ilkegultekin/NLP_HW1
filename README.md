# CMPE 561 Natural Language Processing 2016 Spring Homework 1

This repository contains the implementation of a naive bayes text classifier by Ilke Gultekin

## How to compile and run main.py

- From the command line, go to the directory where main.py resides
- Run the following command "python main.py"

## Parameters

- -f (--function) FUNCTION : There are two functions you can call, "naiveBayes" and "createDataSet", the default value is "naiveBayes"
- -tr (--training) TRAININGSETDIRPATH : This parameter contains the path to the training set directory, needed for the function "naiveBayes"
- -tst (--test) TESTSETDIRPATH : This parameter contains the path to the test set directory, needed for the function "naiveBayes"
- -ds (--dataset) DATASETDIRPATH : This parameter contains the path to the raw data set, needed for the function "createDataSet"
- -tar (--target) TARGETDIRPATH : This parameter contains the path to the target directory that will contain the training and the test data set directories created by the function "createDataSet"
- You can also run python main.py -h in the terminal to get the same information

