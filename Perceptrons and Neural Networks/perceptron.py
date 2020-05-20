import os
import sys
import collections
import re
import math
import copy
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer


class Document:
    line = ""
    word_count = {}
    typey = ""
    guess = ""
    
    def __init__(self, line, counter, typey,guess):
        self.typey = typey
        self.line = line
        self.word_count = counter
        self.learned = guess
        
    def perceptron(trainSet,learnRate, iterations, weights):
        for i in iterations:
            for s in trainSet:
                total =  1
                for we in trainSet[s].word_count:
                    if we not in weights:
                        weights[we] = 0
                    total = total + weights[we] * trainSet[s].word_count[we]
                if trainSet[s].typey == "ham":
                    num = 0
                    if total <= 0:
                        perceptron = 0
                    else:
                        perceptron = 1
                elif trainSet[s].typey == "spam":
                    num = 1
                    if total <= 0:
                        perceptron = 0
                    else:
                        perceptron = 1
                for w in trainSet[s].word_count:
                    weights[w] = weights[w] + float(trainSet[s].word_count[w]) * float(learnRate) * float((num - perceptron))
                
    def filesToLoad(file,type,direct):
         for dir_entry in os.listdir(direct):
             dir_entry_path = os.path.join(direct, dir_entry)
             if os.path.isfile(dir_entry_path):
                 with open(dir_entry_path, encoding = "ISO-8859-1") as text_file:
                     text = text_file.read()
                     temp =collections.Counter(re.findall(r'\w+', text))
                     stemmer = PorterStemmer()
                     singles = [stemmer.stem(temp) for temp in temp]
                     file.update({dir_entry_path: Document(text, temp, type,"")})
                     
    def removeStopWords(setWStopWords):
        stopWords = []
        removedSet = copy.deepcopy(setWStopWords)
        for line in open("stopWords.txt", "r"):  # opened in text-mode; all EOLs are converted to '\n'
            line = line.split()
            stopWords.extend(line)
        for i in stopWords:
            for j in removedSet:
                if i in removedSet[j].word_count:
                    del(removedSet[j].word_count[i])
        return removedSet
        
    def guessNums(dataSet,weights):
        guess = 0
        for i in dataSet:
            x = weights['weightValue']
            for z in dataSet[i].word_count:
                if z not in weights:
                    weights[z] = 0
                x = x + weights[z] * dataSet[i].word_count[z]
            if x <= 0:
                dataSet[i].learned = "ham"
                if dataSet[i].typey == dataSet[i].learned:
                    guess += 1
            else:
                dataSet[i].learned = "spam"
                if dataSet[i].typey == dataSet[i].learned:
                    guess += 1
        return guess
        
    def printing(j,s,guessWStop,trainSetWStop,testSetWStop,guessWoutStop,trainSetWOutStop,testSetWOutStop):
        print("Accuracy with StopWords")
        print("Learning Rate: " , float(j),"Epochs", s)
        print("Training Accuracy: " , '{:.3f}'.format(float(guessWStop) / float(len(trainSetWStop))),"Test Accuracy: " , '{:.3f}'.format(float(guessWStop) / float(len(testSetWStop))))
        print("Accuracy without StopWords")
        print("Learning Rate: " , float(j),"Epochs", s)
        print("Training Accuracy:  " , '{:.3f}'.format(float(guessWoutStop) / float(len(trainSetWOutStop))),"Test Accuracy: " , '{:.3f}'.format(float(guessWoutStop) / float(len(testSetWOutStop))))
        
def main():
    trainSetWStop = {}
    testSetWStop = {}
    trainSetWOutStop = {}
    testSetWOutStop = {}
    stopWords = []
    training_set_vocab = []
    training_set_WOut_vocab = []
    guessWStop = 0
    guessWoutStop = 0
    iterations = ['1','2','10','50','200',]
    learnRate = ['0.0001','0.0005','0.1','0.5']
    weights = {'weightValue': 1.0}
    WOutWeights = copy.deepcopy(weights)
    
    Document.filesToLoad(trainSetWStop,"spam",sys.argv[1])
    Document.filesToLoad(trainSetWStop,"ham",sys.argv[2])
    Document.filesToLoad(testSetWStop,"spam",sys.argv[3])
    Document.filesToLoad(testSetWStop,"ham",sys.argv[4])
    trainSetWOutStop = Document.removeStopWords(trainSetWStop)
    testSetWOutStop = Document.removeStopWords(testSetWStop)
    
    for j in learnRate:
        for s in iterations:
            Document.perceptron(trainSetWStop,j,s,weights)
            Document.perceptron(trainSetWOutStop,j,s,WOutWeights)
            guessWStop = Document.guessNums(testSetWStop,weights)
            guessWoutStop = Document.guessNums(testSetWOutStop,WOutWeights)
            Document.printing(j,s,guessWStop,trainSetWStop,testSetWStop,guessWoutStop,trainSetWOutStop,testSetWOutStop)
            
if __name__ == '__main__':
    main()
