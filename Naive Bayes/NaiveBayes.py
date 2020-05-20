import os
import sys
import collections
import re
import math
import copy
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer

class Document:
    line = ""
    word_count = {}
    typey = ""
    trained = ""

    def __init__(self, line, counter, typey):
        self.typey = typey
        self.line = line
        self.word_count = counter

    def constType(self,type):
        if(type == "line"):
            return self.line
        if(type == "word_count"):
            return self.word_count
        if(type == "trained"):
            return self.trained
        if type == "typey":
            return self.typey

    def setTrained(self, guess):
        self.trained = guess

    def NaiveBayes(training, priors, prob,type):
        if(type=="nb"):
            all_text = ""
            types = ["spam", "ham"]
            for x in training:
                all_text = all_text + training[x].constType("line")
            temp = collections.Counter(re.findall(r'\w+', all_text))
            n = len(training)
            for type in types:
                n_type = 0
                text_type = ""
                for i in training:
                    if training[i].constType("typey") == type:
                        n_type += 1
                        text_type += training[i].constType("line")
                priors[type] = float(n_type) / float(n)
                token_freqs = collections.Counter(re.findall(r'\w+', text_type))
                for t in temp:
                    if t in token_freqs:
                        prob.update({t + "_" + type: (float((token_freqs[t] + 1.0)) / float((len(text_type) + len(token_freqs))))})
                    else:
                        prob.update({t + "_" + type: (float(1.0) / float((len(text_type) + len(token_freqs))))})
        elif (type == "tnb"):
            score = {}
            types = ["spam", "ham"]
            for c in types:
                score[c] = math.log10(float(priors[c]))
                for t in training.constType("word_count"):
                    if (t + "_" + c) in prob:
                        score[c] += float(math.log10(prob[t + "_" + c]))
            if score["spam"] > score["ham"]:
                return "spam"
            else:
                return "ham"
               
    def filesToLoad(file,type,direct):
         for dir_entry in os.listdir(direct):
             dir_entry_path = os.path.join(direct, dir_entry)
             if os.path.isfile(dir_entry_path):
                 with open(dir_entry_path, encoding = "ISO-8859-1") as text_file:
                     text = text_file.read()
                     temp =collections.Counter(re.findall(r'\w+', text))
                     stemmer = PorterStemmer()
                     singles = [stemmer.stem(temp) for temp in temp]
                     file.update({dir_entry_path: Document(text, temp, type)})
                     
    def stopWordsLoad(file):
        stopWords = []
        for line in open(file, "r"):  # opened in text-mode; all EOLs are converted to '\n'
            line = line.split()
            stopWords.extend(line)
        return stopWords
        
    def removeStopWords(stopWords, setWStopWords):
        removedSet = copy.deepcopy(setWStopWords)
        for i in stopWords:
            for j in removedSet:
                if i in removedSet[j].constType("word_count"):
                    del(removedSet[j].constType("word_count")[i])
        return removedSet
        
def main():
    trainSetWStop = {}
    testSetWStop = {}
    trainSetWOutStop = {}
    testSetWOutStop = {}
    condProb={}
    removedCondProb = {}
    prior = {}
    priorWoutStop = {}
    stopWords = []
    guessWStop = 0
    guessWoutStop = 0

    Document.filesToLoad(trainSetWStop,"spam",sys.argv[1])
    Document.filesToLoad(trainSetWStop,"ham",sys.argv[2])
    Document.filesToLoad(testSetWStop,"spam",sys.argv[3])
    Document.filesToLoad(testSetWStop,"ham",sys.argv[4])
    stopWords = Document.stopWordsLoad("stopWords.txt")

    trainSetWOutStop = Document.removeStopWords(stopWords, trainSetWStop)
    testSetWOutStop = Document.removeStopWords(stopWords, testSetWStop)

    Document.NaiveBayes(trainSetWStop, prior, condProb,"nb")
    Document.NaiveBayes(trainSetWOutStop, priorWoutStop, removedCondProb,"nb")
    
    for i in testSetWStop:
        testSetWStop[i].setTrained(Document.NaiveBayes(testSetWStop[i], prior, condProb,"tnb"))
        if testSetWStop[i].constType("trained") == testSetWStop[i].constType("typey"):
            guessWStop += 1

    for i in testSetWOutStop:
        testSetWOutStop[i].setTrained(Document.NaiveBayes(testSetWOutStop[i], priorWoutStop, removedCondProb,"tnb"))
        if testSetWOutStop[i].constType("trained") == testSetWOutStop[i].constType("typey"):
            guessWoutStop += 1
            
    print ("Accuracy for training:\t\t\t\t" , (float(guessWStop) / float(len(trainSetWStop))))
    print ("Accuracy with stop words:\t\t\t" , (float(guessWStop) / float(len(testSetWStop))))
    print ("Accuracy without stop words:\t\t\t" , (float(guessWoutStop) / float(len(testSetWOutStop))))
    

if __name__ == '__main__':
    main()
