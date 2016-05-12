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

```bash
      python main.py -f createDataSet -ds /Users/Gercek/Downloads/69yazar/raw_texts -tar /Users/Gercek/Desktop/NLP_HW1_Test        
      python main.py -f naiveBayes -tr /Users/Gercek/Desktop/NLP_HW1_Test/trainingSet -tst /Users/Gercek/Desktop/NLP_HW1_Test/testSet
```


    

  
# CMPE 561 Natural Language Processing 2016 Spring Homework 2

This repository contains the Part of Speech tagger implementation using Hidden Markov Models and Viterbi algorithm

## How to compile and run 

- From the command line, go to the directory where the project's source folder resides
- First run the following command "python train_hmm_tagger.py --fileLoc <trainingFilePath> --<tag>", where <trainingFilePath> is the path to the file containing the training set and <tag> can be either cpostag or postag. This will train the hmm tagger and create three txt files which contain the probabilities computed from the training set and it will be used by the next program
- Then run the command "python hmm_tagger.py --testFile <testFilePath> --outputFile <outputFilePath>". This will compute the tags of the test set using the probabilities computed in the previous step
- Finally run the command "python evaluate_hmm_tagger.py --outputFile <outputFilePath> --goldFile <goldFilePath> --<tag>". The last argument specifies which tag should be used in the gold standard file (since the sample you gave us contains both the cpostags and the postags) The program will output the total tag accuracy and the accuracy for each tag separately, as well as the confusion matrix 

