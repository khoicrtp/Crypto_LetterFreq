import copy
import time
import os

import numpy as np
import matplotlib.pyplot as plt

from threading import Thread
import threading
import time

cipher = "NWVKIF UWVYC TWY AFYXAKIL CD QKIWCI UNVCCIKYEP HP EIK QEANLEDDL CDP IWKCE XDFP XDYIP. UNVCCIKYEP'Y AFACAWN LIYAMF, XVHNAYEIL DFNAFI HP UWVYC, KIUIKY CD EIK WY 'XDYIP' WY TINN. EIK QVCAI OWKG, CEKII XAFG WFL QPWF HVCCIKUNAIY, AY YAOANWK CD CEWC DU CEI XDFP YGP YGAOOIK. "
expectedResult = "lauren faust was inspired to create fluttershy by her childhood toy earth pony posey. fluttershy's initial design, published online by faust, refers to her as 'posey' as well. her cutie mark, three pink and cyan butterflies, is similar to that of the pony sky skimmer."
cipherTest = "abca"


def defineLetterDict(cipher):
    res = dict()
    for i in range(0, len(cipher)):
        if (cipher[i] not in res and cipher[i].isalpha() == True):
            obj = {cipher[i]: countFreq(cipher, cipher[i])}
            res.update(obj)
    result = sorted(res.items(), key=lambda x: x[1], reverse=True)
    return result

def defineLetterList(cipher):
    res = []
    letterDict=defineLetterDict(cipher)
    for i in range(0, len(letterDict)):
        res.append(letterDict[i][0])
    #print(res)
    return res

def manualReplaceSolve(cipher):
    res = ""
    letterList = defineLetterList(cipher)
    expectedLetters = copy.deepcopy(letterList)
    for i in range(0, len(letterList)):
        if (letterList[i].isalpha() == True):
            temp = "Value for letter "+letterList[i]+": "
            expectedLetters[i] = input(temp)
        else:
            expectedLetters[i] = letterList[i]
    #print(expectedLetters)
    for i in range(0, len(cipher)):
        for j in range(0, len(letterList)):
            if(cipher[i] == letterList[j]):
                res += expectedLetters[j]
                break
    #print("expected output: ", res)
    print("CIPHER TEXT: ", cipher, "\n")

    print("DECODED OUTPUT: ", res, "\n")

    print("EXPECTED OUTPUT:", expectedResult)
    return res

# replace(cipher)


standardLetterFreq = ['e', 't', 'a', 'o', 'i',
                      'n', 's', 'h', 'r', 'd',
                      'l', 'c', 'u', 'm', 'w',
                      'f', 'g', 'y', 'p', 'b',
                      'v', 'k', 'j', 'x', 'q', 'z']


def countFreq(cipher, letter):
    count = 0
    for i in range(0, len(cipher)):
        if letter == cipher[i]:
            count += 1
    return count

def toArray(cipher):
    a = []
    for i in range(0, len(cipher)):
        a.append(cipher[i])
    return a


def toString(a):
    res = ""
    for i in range(len(a)):
        res += a[i]
    return res


def get_nth_key(dictionary, n=0):
    if n < 0:
        n += len(dictionary)
    for i, key in enumerate(dictionary.keys()):
        if i == n:
            return key
    raise IndexError("dictionary index out of range")


def cipherLetterFreqSolve(cipher):
    letterDict = defineLetterDict(cipher)
    expectedLetterDict = dict()
    j = 0
    for i in range(len(letterDict)):
        if(letterDict[i][0].isalpha() == True):
            expectedLetterDict[letterDict[i][0]] = standardLetterFreq[j]
            j += 1
        else:
            expectedLetterDict[letterDict[i][0]] = letterDict[i][0]

    res = toArray(cipher)

    for i in range(0, len(res)):
        for j in range(len(expectedLetterDict)):
            if(cipher[i] == letterDict[j][0]):
                key = get_nth_key(expectedLetterDict, j)
                res[i] = expectedLetterDict[key]
                break
    result = toString(res)

    return result

##DRAW
def getObjKeys(data):
    res=list()
    for i in range(len(data)):
        res.append(data[i][0])
    return res

def getObjValues(data):
    res=list()
    for i in range(len(data)):
        res.append(data[i][1])
    return res

def drawGraph():
    # creating the dataset
    wordList = defineLetterDict(cipher)
    courses = getObjKeys(wordList)
    values = getObjValues(wordList)

    fig = plt.figure(figsize=(10, 5))

# creating the bar plot
    plt.bar(courses, values, color='maroon',
        width=0.4)

    plt.xlabel("Letter")
    plt.ylabel("Frequency")
    plt.title("LETTER FREQUENCY")
    plt.show()

if __name__=='__main__':
    t1=threading.Thread(target=drawGraph, args=())
    t1.start()
    time.sleep(3)
    os.system('cls||clear')
    wordList = defineLetterDict(cipher)
    print("WORDLIST FREQ:", wordList)
    print("STANDARD LETTER FREQ:", standardLetterFreq)
    mode=int(input("CHOOSE MODE:\n1.Manual\n2.Automatic\n"))
    if mode==1:
        t2=threading.Thread(target=manualReplaceSolve, args=(cipher,))

    #manualReplaceSolve(cipher)
    t2.start()
    