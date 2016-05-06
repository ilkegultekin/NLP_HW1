
import math
import argparse

class Cell:
    def __init__(self, _word , _tag, _prob, _prevCellPtr):
        self.word = _word
        self.tag = _tag
        self.prob = _prob
        self.prevCellPtr = _prevCellPtr
    
    def __str__(self):
        return self.word.encode('UTF-8') + ' ' + self.tag + ' ' + str(self.prob)
    
    __repr__ = __str__



wordProbsPerTag = {}
tagProbs = {}
tagProbs['start'] = {}
overallTagFreqs = {}
overallTagProbs = {}
possibleTags = []
def readTaggerFiles():
    overallTagFreqsFileHandle = open('overallTagFrequencies.txt', 'r')
    lines = overallTagFreqsFileHandle.readlines()
    for line in lines:
        splitLine = line.split()
        tag = splitLine[0]
        tagFreq = int(splitLine[1])
        possibleTags.append(tag)
        wordProbsPerTag[tag] = {}
        tagProbs[tag] = {}
        overallTagFreqs[tag] = tagFreq
    
    wordProbsFileHandle = open('wordProbs.txt', 'r')
    lines = wordProbsFileHandle.readlines()
    for line in lines:
        splitLine = line.split()
        tag = splitLine[0]
        word = splitLine[1]
        freq = int(splitLine[2])
        wordProbsPerTag[tag].update({word: freq})
    
    tagProbsFileHandle = open('tagProbs.txt', 'r')
    lines = tagProbsFileHandle.readlines()
    for line in lines:
        splitLine = line.split()
        prevTag = splitLine[0]
        curTag = splitLine[1]
        freq = int(splitLine[2])
        tagProbs[prevTag].update({curTag: freq})
    
    overallTagFreqs['start'] = sum(tagProbs['start'].values())
    #print sum(tagProbs['start'].values())

def convertFreqsToProbs():
    tagProbKeys = tagProbs.keys()
    for key in tagProbKeys:
        totalTagFreq = overallTagFreqs[key]
        for key2 in tagProbs[key].keys():
            tagProbs[key][key2] = math.log(tagProbs[key][key2]/float(totalTagFreq))
    
    wordProbsPerTagKeys = wordProbsPerTag.keys()
    for key in wordProbsPerTagKeys:
        totalTagFreq = overallTagFreqs[key]
        for key2 in wordProbsPerTag[key].keys():
            wordProbsPerTag[key][key2] = math.log(wordProbsPerTag[key][key2]/float(totalTagFreq))
            
    totalTagCount = float(sum(overallTagFreqs.values()))
    for key in overallTagFreqs.keys():
        overallTagProbs[key] = math.log(overallTagFreqs[key]/totalTagCount)
        
def hmm_tagger(testFilePath, outputFile):        

    readTaggerFiles()
    convertFreqsToProbs()
    
    matchingTagCount = 0
    totalTagCount = 0
    actualTagPointer = 0
    actualTagList = []
    
    #testFilePath = '/Users/Gercek/Downloads/metu_sabanci_cmpe_561_v2/validation/turkish_metu_sabanci_val.conll'
    
    testFileHandle = open(testFilePath,'r')
    lines = testFileHandle.readlines()
    sentenceList = []
    
    curSentence = []
    for line in lines:
        if line == '\n':
            sentenceList.append(curSentence)
            curSentence = []
            continue
        word = line.split()[1].decode('UTF-8').lower()        
        if word == '_' or line.split()[3] == 'Punc':
            continue
        curSentence.append(word)
        actualTagList.append(line.split()[3])
    
    unknownProbCoef = 10 
    outputFileHandle = open(outputFile, 'w') 
    #s = sentenceList[1]
    for t in possibleTags:
        outputFileHandle.write(t + ' ')
    outputFileHandle.write('\n')
    
    for s in sentenceList:
        prevColumn = []
        for word in s:
            curColumn = []
            if prevColumn == []:
                prevTag = 'start'
                for tag in possibleTags:
                    if tag not in tagProbs[prevTag]:
                        continue
                    elif word not in wordProbsPerTag[tag]:
                        cellProb = unknownProbCoef*overallTagProbs[tag]
                    else:
                        wordEmissionProb = wordProbsPerTag[tag][word]
                        tagTransitionProb = tagProbs[prevTag][tag]
                        cellProb = wordEmissionProb + tagTransitionProb
                    c = Cell(word, tag, cellProb, None)
                    curColumn.append(c)
                prevColumn = curColumn
            else:
                for tag in possibleTags:
                    if word not in wordProbsPerTag[tag]:
                        probDict = {}
                        for cell in prevColumn:
                            prevTag = cell.tag
                            if tag not in tagProbs[prevTag]:
                                continue
                            prevCellProb = cell.prob
                            cellProb = prevCellProb + unknownProbCoef*overallTagProbs[tag]
                            probDict[cellProb] = cell
                        maxProb = max(probDict.keys())
                        prevCellPtr = probDict[maxProb]
                        c = Cell(word, tag, maxProb, prevCellPtr)
                        curColumn.append(c) 
                    else:
                        probDict = {}
                        wordEmissionProb = wordProbsPerTag[tag][word]
                        for cell in prevColumn:
                            prevTag = cell.tag
                            if tag not in tagProbs[prevTag]:
                                continue
                            prevCellProb = cell.prob
                            tagTransitionProb = tagProbs[prevTag][tag]
                            curProb = wordEmissionProb + tagTransitionProb + prevCellProb
                            probDict[curProb] = cell
                        maxProb = max(probDict.keys())
                        prevCellPtr = probDict[maxProb]
                        c = Cell(word, tag, maxProb, prevCellPtr)
                        curColumn.append(c)
                prevColumn = curColumn
    
    
        tag = 'end'
        probDict = {}
        for cell in prevColumn:
            prevTag = cell.tag
            if tag not in tagProbs[prevTag]:
                continue
            prevCellProb = cell.prob
            tagTransitionProb = tagProbs[prevTag][tag]
            curProb = prevCellProb + tagTransitionProb
            probDict[curProb] = cell
        maxProb = max(probDict.keys())
        prevCellPtr = probDict[maxProb]
        c = Cell(word, tag, maxProb, prevCellPtr)
        
        cellQueue = []
        while c.prevCellPtr:
            cellQueue.append(c.prevCellPtr)
            c = c.prevCellPtr
        for i in range(len(cellQueue)-1,-1,-1):
            curCell = cellQueue[i]
            outputFileHandle.write(curCell.word.encode('UTF-8') + ' ' + curCell.tag + '\n')
            
            totalTagCount += 1
            if curCell.tag == actualTagList[actualTagPointer]:
                matchingTagCount += 1
            actualTagPointer += 1
        
        outputFileHandle.write('\n')
    
    print 'bitti'
    print matchingTagCount
    print totalTagCount
    print matchingTagCount/float(totalTagCount)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-tst', '--testFile', default="/Users/Gercek/Downloads/metu_sabanci_cmpe_561_v2/validation/turkish_metu_sabanci_val.conll", type=str, help='test file location')
    parser.add_argument('-out', '--outputFile', default='output.txt', type=str, help='output file path')
    opts = parser.parse_args()
    hmm_tagger(opts.testFile, opts.outputFile)


        
        
        
         

        

# print [cell for cell in curColumn]
# for i in range(len(curColumn)):
#     print i
#     print curColumn[i]
# 


                
            
        
        
        
        
        
        







        
    