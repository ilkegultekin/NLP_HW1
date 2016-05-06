
import argparse

def evaluate_hmm_tagger(outputFile, testFilePath, cpostagFlag, postagFlag):

    testFilePath = '/Users/Gercek/Downloads/metu_sabanci_cmpe_561_v2/validation/turkish_metu_sabanci_val.conll'
    
    testFileHandle = open(testFilePath, 'r')
    outputFileHandle = open('output.txt', 'r')
    
    possibleTags = outputFileHandle.readline().split()
    
    outputLines = outputFileHandle.readlines()
    
    nextTestLine = testFileHandle.readline()
    confusionMatrix = {}
    if cpostagFlag:
        cposOrPos = 3
    elif postagFlag:
        cposOrPos = 4
    else:
        print 'invalid tagset information'
        return
    
    correctTagCount = 0
    totalTagCount = 0
    
    for t in possibleTags:
        confusionMatrix[t] = {}
        for t2 in possibleTags:
            confusionMatrix[t][t2] = 0
    
    for outputLine in outputLines:
        if outputLine == '\n':
            continue
        outputLineList = outputLine.split()
        #word = outputLineList[0]
        tag = outputLineList[1]
        while nextTestLine == '\n':
            nextTestLine = testFileHandle.readline()
        testLineList = nextTestLine.split()
        while testLineList[1] == '_' or testLineList[3] == 'Punc':
            nextTestLine = testFileHandle.readline()
            testLineList = nextTestLine.split()
            if nextTestLine == '\n':
                nextTestLine = testFileHandle.readline()
                testLineList = nextTestLine.split()
        #testWord = testLineList[1].lower()
        testTag = testLineList[cposOrPos]
        totalTagCount += 1
    #     if word == testWord:
        confusionMatrix[testTag][tag] += 1
        if tag == testTag:
            correctTagCount += 1
        nextTestLine = testFileHandle.readline()
    
    print confusionMatrix
    print 'correct tag count : %d' % correctTagCount
    print 'total tag count : %d' % totalTagCount
    print 'total tag accuracy : %.2f' % (correctTagCount/float(totalTagCount))
    
    for t in possibleTags:
        totalTagCountForTag = float(sum(confusionMatrix[t].values()))
        if not totalTagCountForTag:
            print 'tag %s not found in gold standard file' % t
        else:
            print 'tag accuracy for tag %s : %.2f' % (t, confusionMatrix[t][t]/totalTagCountForTag)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-out', '--outputFile', default='output.txt', type=str, help='output file path')
    parser.add_argument('-gold', '--goldFile', default="/Users/Gercek/Downloads/metu_sabanci_cmpe_561_v2/validation/turkish_metu_sabanci_val.conll", type=str, help='gold standard file location')
    parser.add_argument('--cpostag', help='the cpostag field  will be used for comparison if this flag is true', action='store_true')
    parser.add_argument('--postag', help='the postag field will be used for comparison if this flag is true', action='store_true')
    opts = parser.parse_args()
    evaluate_hmm_tagger(opts.outputFile, opts.goldFile, opts.cpostag, opts.postag)
    
        
    
    
    

