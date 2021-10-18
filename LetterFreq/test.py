import copy
import pickle
import gib_detect_train

import numpy as np
import matplotlib.pyplot as plt

model_data = pickle.load(open('gib_model.pki', 'rb'))
cipher = "NWVKIF UWVYC TWY AFYXAKIL CD QKIWCI UNVCCIKYEP HP EIK QEANLEDDL CDP IWKCE XDFP XDYIP. UNVCCIKYEP'Y AFACAWN LIYAMF, XVHNAYEIL DFNAFI HP UWVYC, KIUIKY CD EIK WY 'XDYIP' WY TINN. EIK QVCAI OWKG, CEKII XAFG WFL QPWF HVCCIKUNAIY, AY YAOANWK CD CEWC DU CEI XDFP YGP YGAOOIK. "
expectedResult = "lauren faust was inspired to create fluttershy by her childhood toy earth pony posey. fluttershy's initial design, published online by faust, refers to her as 'posey' as well. her cutie mark, three pink and cyan butterflies, is similar to that of the pony sky skimmer."
cipherTest = "abca"


def countFreq(cipher, letter):
    count = 0
    for i in range(0, len(cipher)):
        if letter == cipher[i]:
            count += 1
    return count


def defineLetterDict(cipher):
    res = dict()
    for i in range(0, len(cipher)):
        if (cipher[i] not in res and cipher[i].isalpha() == True):
            obj = {cipher[i]: countFreq(cipher, cipher[i])}
            res.update(obj)
    result = sorted(res.items(), key=lambda x: x[1], reverse=True)
    return result


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


standardLetterFreq = ['e', 't', 'a', 'o', 'i',
                      'n', 's', 'h', 'r', 'd',
                      'l', 'c', 'u', 'm', 'w',
                      'f', 'g', 'y', 'p', 'b',
                      'v', 'k', 'j', 'x', 'q', 'z']


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

def drawGraph(data):
    # creating the dataset
    courses = getObjKeys(data)
    values = getObjValues(data)

    fig = plt.figure(figsize=(10, 5))

# creating the bar plot
    plt.bar(courses, values, color='maroon',
        width=0.4)

    plt.xlabel("Letter")
    plt.ylabel("Frequency")
    plt.title("LETTER FREQUENCY")
    plt.show()

# wordList = defineLetterDict(cipher)
# print("WORDLIST:", wordList)
# print(wordList[0][0])
# #drawGraph(wordList)
# cipherArray = toArray(cipher)
# dummyArray = createDummyArray(cipher)
# toWordList = standardLetterFreq
# deny = []
# Result=recurReplace(cipherArray, dummyArray, wordList, toWordList, deny)

#printResult(dummyArray)
a=[1]
a1=1
b=[2,3,4,5]
def appendArray(a, b):
    for i in range(len(b)):
        a.append(b[i])
appendArray(a, b)
print(a)
