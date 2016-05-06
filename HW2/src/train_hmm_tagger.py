
import argparse

def train_hmm_tagger(trainFilePath, cpostagFlag, postagFlag):
    tagProbs = {}
    wordProbsPerTag = {}
    overallTagFreqs = {}
#     trainFilePath = '/Users/Gercek/Downloads/metu_sabanci_cmpe_561_v2/train/turkish_metu_sabanci_train.conll'
    trainFileHandle = open(trainFilePath,'r')
    lines = trainFileHandle.readlines()
    
    
    formOrLemma = 1 #1=form, 2=lemma
    if cpostagFlag:
        cposOrPos = 3
    elif postagFlag:
        cposOrPos = 4
    else:
        print 'invalid tagset information'
        return
    #cposOrPos = 3 #3=cpos, 4=pos
    
    prevTag = 'start'
    for line in lines:
        if line == '\n':
            tag = 'end'
            if prevTag in tagProbs:
                if tag in tagProbs[prevTag]:
                    tagProbs[prevTag][tag] += 1
                else:
                    tagProbs[prevTag][tag] = 1
            else:
                tagProbs[prevTag] = {tag: 1}
                
            prevTag = 'start'
            continue
        
        splitLine = line.split()
        
        if splitLine[formOrLemma] == '_' or splitLine[cposOrPos] == 'Punc':
            continue
        
        tag = splitLine[cposOrPos]
        if tag in overallTagFreqs:
            overallTagFreqs[tag] += 1
        else:
            overallTagFreqs[tag] = 1
        
        word = splitLine[formOrLemma].decode('UTF-8').lower()
        
        if tag in wordProbsPerTag:
            if word in wordProbsPerTag[tag]:
                wordProbsPerTag[tag][word] += 1
            else:
                wordProbsPerTag[tag][word] = 1
        else:
            wordProbsPerTag[tag] = {word: 1}
        
        if prevTag in tagProbs:
            if tag in tagProbs[prevTag]:
                tagProbs[prevTag][tag] += 1
            else:
                tagProbs[prevTag][tag] = 1
        else:
            tagProbs[prevTag] = {tag: 1}
        prevTag = tag
        
#     possibleTags = wordProbsPerTag.keys()
#     possibleTagsFileHandle = open('possibleTags.txt', 'w')
#     for tag in possibleTags:
#         possibleTagsFileHandle.write(tag + '\n')
            
    wordProbsFileHandle = open('wordProbs.txt', 'w')
    keys = wordProbsPerTag.keys()
    for tag in keys:
        wordProbDict = wordProbsPerTag[tag]
        for word in wordProbDict.keys():
            freq = str(wordProbDict[word])
            word = word.encode('UTF-8')
            wordProbsFileHandle.write(tag + ' ' + word + ' ' + freq + '\n')
    
    tagProbsFileHandle = open('tagProbs.txt', 'w')
    keys = tagProbs.keys()
    for prevTag in keys:
        tagProbDict = tagProbs[prevTag]
        for tag in tagProbDict.keys():
            freq = str(tagProbDict[tag])
            tagProbsFileHandle.write(prevTag + ' ' + tag + ' ' + freq + '\n') 
    
    overallTagFreqsFileHandle = open('overallTagFrequencies.txt', 'w')
    keys = overallTagFreqs.keys()
    for key in keys:
        overallTagFreqsFileHandle.write(key + ' ' + str(overallTagFreqs[key]) + '\n')
    
    
    
        

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-fl', '--fileLoc', default="/Users/Gercek/Downloads/metu_sabanci_cmpe_561_v2/train/turkish_metu_sabanci_train.conll", type=str, help='training file location')
    parser.add_argument('--cpostag', help='the cpostag field will be used if this flag is true', action='store_true')
    parser.add_argument('--postag', help='the postag field will be used if this flag is true', action='store_true')
    #parser.add_argument('-ts', '--tagSet', default='cpostag', type=str, help='tagset can be cpostag or postag')
    opts = parser.parse_args()
    train_hmm_tagger(opts.fileLoc, opts.cpostag, opts.postag)
    #train_hmm_tagger('/Users/Gercek/Downloads/metu_sabanci_cmpe_561_v2/train/turkish_metu_sabanci_train.conll', 'cpostag')        

    
    
    
    
    