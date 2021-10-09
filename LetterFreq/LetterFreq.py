import copy
import pickle
import gib_detect_train

model_data = pickle.load(open('gib_model.pki', 'rb'))
cipher = "NWVKIF UWVYC TWY AFYXAKIL CD QKIWCI UNVCCIKYEP HP EIK QEANLEDDL CDP IWKCE XDFP XDYIP. UNVCCIKYEP'Y AFACAWN LIYAMF, XVHNAYEIL DFNAFI HP UWVYC, KIUIKY CD EIK WY 'XDYIP' WY TINN. EIK QVCAI OWKG, CEKII XAFG WFL QPWF HVCCIKUNAIY, AY YAOANWK CD CEWC DU CEI XDFP YGP YGAOOIK. "
expectedResult = "lauren faust was inspired to create fluttershy by her childhood toy earth pony posey. fluttershy's initial design, published online by faust, refers to her as 'posey' as well. her cutie mark, three pink and cyan butterflies, is similar to that of the pony sky skimmer."
cipherTest = "abca"

def checkValidWord(word):
    model_mat = model_data['mat']
    threshold = model_data['thresh']
    return (gib_detect_train.avg_transition_prob(word, model_mat) > threshold)

def defineLetterList(cipher):
    res = []
    for i in range(0, len(cipher)):
        if (cipher[i] not in res):
            res.append(cipher[i])
    return res


def replace(cipher):
    res = ""
    letterList = defineLetterList(cipher)
    expectedLetters = copy.deepcopy(letterList)
    for i in range(0, len(letterList)):
        if (letterList[i].isalpha() == True):
            temp = "Value for letter "+letterList[i]+": "
            expectedLetters[i] = input(temp)
        else:
            expectedLetters[i] = letterList[i]
    print(expectedLetters)
    for i in range(0, len(cipher)):
        for j in range(0, len(letterList)):
            if(cipher[i] == letterList[j]):
                res += expectedLetters[j]
                break
    print("expected output: ", res)
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


def defineLetterDict(cipher):
    res = dict()
    for i in range(0, len(cipher)):
        if (cipher[i] not in res):
            obj = {cipher[i]: countFreq(cipher, cipher[i])}
            res.update(obj)
    result = sorted(res.items(), key=lambda x: x[1], reverse=True)
    return result


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


print("CIPHER TEXT: ", cipher, "\n")

print("DECODED OUTPUT: ", cipherLetterFreqSolve(cipher), "\n")

print("EXPECTED OUTPUT:", expectedResult)

print(checkValidWord("sui"))