#!/usr/bin/env python
# -*- coding: utf-8 -*-

from random import randint
import os
import string
import shutil
import argparse
import math
import operator


def cleanDirectory(dirPath):
    for fileName in os.listdir(dirPath):
        if fileName == '.DS_Store':
            continue
        os.remove(dirPath + "/" + fileName)

def createDataSetDirectory(fileDirPath, targetDirPath):
    if not os.path.isdir(targetDirPath):
        os.mkdir(targetDirPath)
    fileDirList = [x for x in os.listdir(fileDirPath) if x != '.DS_Store']
    trainingDir = targetDirPath + "/trainingSet"
    testDir = targetDirPath + "/testSet"
    if not os.path.isdir(trainingDir):
        os.mkdir(trainingDir)
    if not os.path.isdir(testDir):
        os.mkdir(testDir)
    for directory in fileDirList:
        currentAuthorTrainDir = trainingDir + "/" + directory
        currentAuthorTestDir = testDir + "/" + directory
        if not os.path.isdir(currentAuthorTrainDir):
            os.mkdir(currentAuthorTrainDir)
        if not os.path.isdir(currentAuthorTestDir):
            os.mkdir(currentAuthorTestDir)
    
    return trainingDir, testDir

def createDataSets(fileDirPath, trainSetDirPath, testSetDirPath):
    #trainingSet = {}
    #testSet = {}
    dirList = [x for x in os.listdir(fileDirPath) if x != '.DS_Store']
    for directory in dirList:
        dirFullPath = createFullPathFromDir(fileDirPath, directory)
        authorTrainSetPath = trainSetDirPath + "/" + directory
        authorTestSetPath = testSetDirPath + "/" + directory
        cleanDirectory(authorTrainSetPath)
        cleanDirectory(authorTestSetPath)
        createDataSetsForEachAuthor(dirFullPath, authorTrainSetPath, authorTestSetPath)

def createDataSetsForEachAuthor(dirPath, authorTrainSetPath, authorTestSetPath):
    fileList = os.listdir(dirPath)
    fileCount = len(fileList)
    trainFileCount = fileCount*0.6
    testFileCount = fileCount - trainFileCount
    #trainingText = ''
    #testText = ''
    while len(fileList) > testFileCount:
        rnd = randint(0,len(fileList)-1)
        fileFullPath = createFullPathFromDir(dirPath, fileList[rnd])
        shutil.copy(fileFullPath, authorTrainSetPath)
        #f = open(fileFullPath,'r')
        #text = preprocessText(f.read()).decode('ISO 8859-9')
        #trainingText += text
        del fileList[rnd]
    
    for f in fileList:
        fileFullPath = createFullPathFromDir(dirPath, f)
        shutil.copy(fileFullPath, authorTestSetPath)
        #f = open(fileFullPath,'r')
        #text = preprocessText(f.read()).decode('ISO 8859-9')
        #testText = testText + " " + text
    
    
    #f = open('/Users/Gercek/Desktop/test.txt','w')
    #f.write(trainingText.encode('UTF-8'))
    
    #trainingSet[className] = tokenize(trainingText)
    #testSet[className]= testText
    
    #print trainingText
    
def createDictForEachAuthor(dirPath):
    authorBags = {}
    dirList = [x for x in os.listdir(dirPath) if x != '.DS_Store']
    for directory in dirList:
        authorBags[directory] = {}
    
    

def createFullPathFromDir(dirPath, current):
    return dirPath + '/' + current

def preprocessText(text):
    txtWoPunc = str(text).translate(None, string.punctuation)
    return txtWoPunc
    
def tokenize(text, dictionary):
    txtLower = text.lower()
    wordCount = 0
    wordList = txtLower.split()
    for w in wordList:
        wordCount += 1
        w2 = w.encode('UTF-8')
        if w2 in dictionary:
            dictionary[w2] += 1
        else:
            dictionary[w2] = 1
    
    return wordCount
#     for word in wordList:
#         print word
#     dictio = {}
#     f = open('/Users/Gercek/Desktop/test.txt','w')
#     f.write(text.encode('UTF-8'))
#     wordList = text.split()
#     for word in wordList:
#         if word in dictio:
#             dictio[word] += 1
#         else:
#             dictio[word] = 1
#     
#     sortedDict = sorted(dictio.items(), key=operator.itemgetter(1))
# 
#     f = open('/Users/Gercek/Desktop/test2.txt','w')
#     for k in sortedDict:
#         f.write(k[0].encode("UTF-8"))
#         f.write("---")
#         f.write(str(k[1]))
#         f.write("\n") 

def naiveBayes(trainingSetPath, testSetPath):
    authorList = []
    dictionary = {}
    wordCountPerAuthor = {}
    results = {}
    priors = calculatePriors(trainingSetPath)
    dList = [x for x in os.listdir(trainingSetPath) if x != '.DS_Store']
    for d in dList:
        totalWordCountPerAuthor = 0
        authorList.append(d)
        dictionary[d] = {}
        dirFullPath = createFullPathFromDir(trainingSetPath, d)
        fList = [x for x in os.listdir(dirFullPath) if x != '.DS_Store']
        for f in fList:
            fileFullPath = createFullPathFromDir(dirFullPath, f)
            fHandler = open(fileFullPath,'r')
            #text = preprocessText(fHandler.read())
            text = preprocessText(fHandler.read()).decode('ISO 8859-9')
            docWordCount = tokenize(text, dictionary[d])
            totalWordCountPerAuthor += docWordCount
        wordCountPerAuthor[d] = totalWordCountPerAuthor
    vocab = generateVocab(dictionary)
    vocabLen = len(vocab)
    
    for author in authorList:
        dirFullPath = createFullPathFromDir(testSetPath, author)
        docListForAuthor = [x for x in os.listdir(dirFullPath) if x != '.DS_Store']
        for doc in docListForAuthor:
            fileFullPath = createFullPathFromDir(dirFullPath, doc)
            fHandler = open(fileFullPath,'r')
            text = preprocessText(fHandler.read()).decode('ISO 8859-9').lower()
            wordList = text.split()
            #maxProb = -100000000
            authorProbs = priors.values()
            for word in wordList:
                wordUTF8 = word.encode('UTF-8')
                for i in xrange(len(authorList)):
                    author2 = authorList[i]
                    currentDict = dictionary[author2]
                    totalWordCount = wordCountPerAuthor[author2] + (vocabLen*0.1)
                    try:
                        wordFreq = currentDict[wordUTF8] + 0.1
                    except KeyError:
                        wordFreq = 1
                    authorProbs[i] += math.log(float(wordFreq)/totalWordCount)
                    
            index, value = max(enumerate(authorProbs), key=operator.itemgetter(1))
            classResult = authorList[index]
            results[(author,doc)] = (author, classResult)
            #print "(" + author + doc + ")" + " --- " + author + " --- " + classResult
            
    computeEvaluationMetrics(authorList, results)
                        
#             for author2 in authorList:
#                 totalProb = 0
#                 currentDict = dictionary[author2]
#                 authorPrior = priors[author2]
#                 totalWordCount = wordCountPerAuthor[author2] + vocabLen
#                 for word in wordList:
#                     wordUTF8 = word.encode('UTF-8')
#                     if wordUTF8 in currentDict.keys():
#                         wordFreq = currentDict[wordUTF8] + 1
#                     else:
#                         wordFreq = 1
#                     totalProb += math.log(float(wordFreq)/totalWordCount)
#                 if totalProb > maxProb:
#                     maxProb = totalProb
#                     classResult = author2
            
            
def computeEvaluationMetrics(authorList, results):
    authorContDict = {}
    for author in authorList:
        contingencyDict = {'tp' : 0, 'fp': 0, 'fn': 0}
        for val in results.values():
            docAuthor = val[0]
            resultAuthor = val[1]
            if author == docAuthor and author == resultAuthor:
                contingencyDict['tp'] += 1
            elif author == docAuthor and author != resultAuthor:
                contingencyDict['fn'] += 1
            elif author != docAuthor and author == resultAuthor:
                contingencyDict['fp'] += 1
        tp = contingencyDict['tp']
        fp = contingencyDict['fp']
        fn = contingencyDict['fn']
        try:
            precision = float(tp)/(tp+fp)
        except ZeroDivisionError:
            precision = 0
        recall = float(tp)/(tp+fn)
        try:
            fMeasure = (2*precision*recall)/(precision+recall)
        except ZeroDivisionError:
            fMeasure = 0
        contingencyDict["precision"] = precision
        contingencyDict["recall"] = recall
        contingencyDict["fMeasure"] = fMeasure
        authorContDict[author] = contingencyDict
    
    macroResults = macroAverage(authorContDict)
    microResults = microAverage(authorContDict)
    print "macroResults: " + str(macroResults)
    print "microResults: " + str(microResults)
            
def macroAverage(authorContDict):
    pTotal = 0
    rTotal = 0
    fTotal = 0
    authorCount = len(authorContDict.keys())
    for dct in authorContDict.values():
        pTotal += dct["precision"]
        rTotal += dct["recall"]
        fTotal += dct["fMeasure"]
    return float(pTotal)/authorCount, float(rTotal)/authorCount, float(fTotal)/authorCount

def microAverage(authorContDict):
    tp = 0
    fp = 0
    fn = 0
    for dct in authorContDict.values():
        tp += dct["tp"]
        fp += dct["fp"]
        fn += dct["fn"]
    try:
        precision = float(tp)/(tp+fp)
    except ZeroDivisionError:
        precision = 0
    recall = float(tp)/(tp+fn)
    try:
        fMeasure = (2*precision*recall)/(precision+recall)
    except ZeroDivisionError:
        fMeasure = 0
    
    return precision, recall, fMeasure
        
                
                   
                
        

def generateVocab(dct):
    vocSet = set([])
    for wordDct in dct.values():
        wordSet = set(wordDct.keys())
        vocSet = vocSet | wordSet
    
    return vocSet

def calculatePriors(trainingSetPath):
    priors = {}
    dList = [x for x in os.listdir(trainingSetPath) if x != '.DS_Store']
    for d in dList:
        dirFullPath = createFullPathFromDir(trainingSetPath, d)
        fList = [x for x in os.listdir(dirFullPath) if x != '.DS_Store']
        priors[d] = math.log(len(fList))
    return priors
        
            


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--function', default="naiveBayes", type=str, help='function to call')
    parser.add_argument('-tr', '--training', default="/Users/Gercek/Downloads/69yazar/trainingSet", type=str, help='training set directory path')
    parser.add_argument('-tst', '--test', default="/Users/Gercek/Downloads/69yazar/testSet", type=str, help='test set directory path')
    parser.add_argument('-ds', '--dataset', default="/Users/Gercek/Downloads/69yazar/raw_texts", type=str, help='data set directory path')
    parser.add_argument('-tar', '--target', default="/Users/Gercek/Downloads/69yazar", type=str, help='target training and test set directory path')
    opts = parser.parse_args()
    if opts.function == "naiveBayes":
        trainingSetPath = opts.training
        testSetPath = opts.test
        from timeit import Timer
        t = Timer(lambda: naiveBayes(trainingSetPath, testSetPath))
        print t.timeit(number=1)
    elif opts.function == "createDataSet":
        dataSetPath = opts.dataset
        targetPath = opts.target
        trainingSetPath, testSetPath = createDataSetDirectory(dataSetPath, targetPath)
        createDataSets(dataSetPath, trainingSetPath, testSetPath)
    else:
        print "No such function"
        
        
    #dirPath = '/Users/Gercek/Downloads/69yazar/raw_texts'
    #trainingSetPath = '/Users/Gercek/Downloads/69yazar/trainingSet'
    #testSetPath = '/Users/Gercek/Downloads/69yazar/testSet'
    
    
    
    #createDataSets(filePath, trainingSetPath, testSetPath)
    #createDataSetDirectory(filePath, dataSetPath)
    #[trainingSet,testSet] = createDataSets(path)
    #tokenize(trainingSet[0])
