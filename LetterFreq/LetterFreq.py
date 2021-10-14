import copy
import time
import os
import numpy as np
import matplotlib.pyplot as plt
from threading import Thread
import threading
import time
import pickle
import gib_detect_train


model_data = pickle.load(open('gib_model.pki', 'rb'))

cipher = "NWVKIF UWVYC TWY AFYXAKIL CD QKIWCI UNVCCIKYEP HP EIK QEANLEDDL CDP IWKCE XDFP XDYIP. UNVCCIKYEP'Y AFACAWN LIYAMF, XVHNAYEIL DFNAFI HP UWVYC, KIUIKY CD EIK WY 'XDYIP' WY TINN. EIK QVCAI OWKG, CEKII XAFG WFL QPWF HVCCIKUNAIY, AY YAOANWK CD CEWC DU CEI XDFP YGP YGAOOIK. "
expectedResult = "lauren faust was inspired to create fluttershy by her childhood toy earth pony posey. fluttershy's initial design, published online by faust, refers to her as 'posey' as well. her cutie mark, three pink and cyan butterflies, is similar to that of the pony sky skimmer."
cipherTest = "abcaade"

standardLetterFreq = ['e', 't', 'a', 'o', 'i',
                      'n', 's', 'h', 'r', 'd',
                      'l', 'c', 'u', 'm', 'w',
                      'f', 'g', 'y', 'p', 'b',
                      'v', 'k', 'j', 'x', 'q', 'z']


def checkValidWord(word):
    model_mat = model_data['mat']
    threshold = model_data['thresh']
    return (gib_detect_train.avg_transition_prob(word, model_mat) > threshold)

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
    for i in range(0, len(cipher)):
        if (cipher[i] not in res):
            res.append(cipher[i]) 
    return res

def inputByFreq(cipher, letterList, expectedLetters):
    res = []
    letterDict=defineLetterDict(cipher)
    for i in range(0, len(letterDict)):
        res.append(letterDict[i][0])

    for i in range(0, len(res)):
        for j in range(0, len(letterList)):
            if (res[i].isalpha() == True):
                if letterList[j]==res[i]:
                    temp = "Value for letter "+res[i]+": "
                    expectedLetters[j] = input(temp)

    return expectedLetters            
    

def manualReplaceSolve(cipher):
    res = ""
    letterList = defineLetterList(cipher)
    expectedLetters = copy.deepcopy(letterList)
    expectedLetters=inputByFreq(cipher, letterList, expectedLetters)

    for i in range(0, len(cipher)):
        for j in range(0, len(letterList)):
            if(cipher[i] == letterList[j]):
                res += expectedLetters[j]
                break
    print("CIPHER TEXT: ", cipher, "\n")

    print("DECODED OUTPUT: ", res, "\n")

    print("EXPECTED OUTPUT:", expectedResult)
    return res

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
    print(result)

    return result

########
## AUTOMATIC
def checkValidWord(word):
    model_mat = model_data['mat']
    threshold = model_data['thresh']
    return (gib_detect_train.avg_transition_prob(word, model_mat) > threshold)

def collectWordList(a):
    wordList = []
    temp = ""
    for i in range(0, len(a)):
        if(a[i] != " " and a[i] != "*" and a[i].isalpha() == True):
            temp += str(a[i])
        else:
            if temp != "":
                wordList.append(temp)
            temp = ""
    wordList.append(temp)

    return wordList

def checkEachWordIsLegit(a):
    wordList = collectWordList(a)
    print("WORDLIST CHECK:", wordList)
    for i in range(0,len(wordList)):
        print(wordList[i]," is:", checkValidWord(wordList[i]))
        if(checkValidWord(wordList[i]) == False):
            return False
    return True


def replaceLetter(cipherArray, dummyArray, letter, toLetter):
    print("REPLACING ",letter, " to ", toLetter)
    for i in range(len(dummyArray)):
        if cipherArray[i] == letter[0]:
            dummyArray[i] = toLetter

    if(checkEachWordIsLegit(dummyArray) == True):
        # print(dummyArray)
        return dummyArray
    else:
        return 0


def toArray(cipher):
    a = []
    for i in range(0, len(cipher)):
        a.append(cipher[i])
    return a


def createDummyArray(cipher):
    a = []
    for i in range(0, len(cipher)):
        if(cipher[i].isalpha() == True):
            a.append('*')
        else:
            a.append(cipher[i])
    return a

def recurReplace(cipherArray, dummyArray, wordList, toWordList, deny):
    if('*' not in dummyArray):
        return dummyArray

    tempDeny=copy.deepcopy(deny)
    tempWordList = copy.deepcopy(wordList)
    tempToWordList = copy.deepcopy(toWordList)
    
    letter = tempWordList[0]
    tempWordList.remove(letter)
    
    toLetter = tempToWordList[0]
    i = 0
    cantReplaceFlag=0
    while(toLetter in tempDeny):
        i += 1
        if i==len(tempToWordList):
            cantReplaceFlag=1
            break
        toLetter = tempToWordList[i]
    if cantReplaceFlag==1:
        temp=wordList[0]
        wordList[0]=wordList[1]
        wordList[1]=temp
        print("SWAPPED: ",wordList)
        cantReplaceFlag=0
        tempDeny=copy.deepcopy(deny)
        return recurReplace(cipherArray, dummyArray, wordList, toWordList, deny)
    tempToWordList.remove(toLetter)

    tempDummy = replaceLetter(cipherArray, dummyArray, letter, toLetter)

    if(tempDummy != 0):
        tempDeny.append(toLetter)
        print("DUMMY:", collectWordList(dummyArray), '\n')
        return recurReplace(cipherArray, tempDummy, tempWordList, tempToWordList, tempDeny)
    else:
        deny.append(toLetter)
        print("DUMMY:", collectWordList(dummyArray), '\n')
        return recurReplace(cipherArray, dummyArray, wordList, toWordList, deny)

def printResult(dummyArray):
    result=collectWordList(dummyArray)
    stringRes=""
    print("CRACKED OUTPUT:")
    for i in range (len(result)):
        stringRes+=result[i]+" "
    print(stringRes)
    return stringRes
########
## DRAW
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

def crackByAI(cipher):
    cipherArray = toArray(cipher)
    dummyArray = createDummyArray(cipher)
    wordList = defineLetterDict(cipher)
    toWordList = standardLetterFreq
    deny = []
    Result=recurReplace(cipherArray, dummyArray, wordList, toWordList, deny)
    printResult(dummyArray)

if __name__=='__main__':
    t1=threading.Thread(target=drawGraph, args=())
    t1.start()
    time.sleep(3)
    os.system('cls||clear')
    wordList = defineLetterDict(cipher)
    print("WORDLIST FREQ:", wordList)
    print("STANDARD LETTER FREQ:", standardLetterFreq)
    mode=int(input("CHOOSE MODE:\n1.Manual\n2.Automatic with pure frequency method\n3.Automatic with AI (Still bugging)\n"))
    while(mode!=1 and mode!=2 and mode!=3):
        print("PLEASE SELECT YOUR OPTION AGAIN")
        mode=int(input())
    if mode==1:
        t2=threading.Thread(target=manualReplaceSolve, args=(cipher,))
        t2.start()
    elif mode==2:
        t2=threading.Thread(target=cipherLetterFreqSolve, args=(cipher,))
        t2.start()
    elif mode==3:
        t2=threading.Thread(target=crackByAI, args=(cipher,))
        t2.start()