import re
import fileinput
import operator
import cipher
from collections import OrderedDict
import sys

class Gram:
    def __init__(self, word, freq):
        self.word = word
        self.freq = freq

def main():
    allWords = []
    for line in fileinput.input(files ='/Users/frankfondell/Documents/test.txt'):
        for word in line.split():
            allWords.append(re.sub('[^a-zA-Z]+', '', word).upper())
    oneLetterWords = []
    firstLetter = []
    lastLetter = []
    onegrams = []
    bigrams = []
    trigrams = []
    quadgrams = []
    doubles = []
    temp = []
    for i in range(len(allWords)):
        if(inList(firstLetter, Gram(allWords[i][0:1], 0))):
            firstLetter[getIndex(firstLetter, Gram(allWords[i][0:1], 0))].freq = firstLetter[getIndex(firstLetter, Gram(allWords[i][0:1], 0))].freq + 1
        else:
            if(allWords[i][0:1]!=""):
                firstLetter.append(Gram(allWords[i][0:1], 1))

        if(allWords[i]!=""):
            if(inList(lastLetter, Gram(allWords[i][-1], 0))):
                lastLetter[getIndex(lastLetter, Gram(allWords[i][-1], 0))].freq = lastLetter[getIndex(lastLetter, Gram(allWords[i][-1], 0))].freq + 1
            else:
                lastLetter.append(Gram(allWords[i][-1], 1))

        if(len(allWords[i])==3):
            if(inList(trigrams, Gram(allWords[i], 0))):
                trigrams[getIndex(trigrams, Gram(allWords[i], 0))].freq = trigrams[getIndex(trigrams, Gram(allWords[i], 0))].freq + 1
            else:
                trigrams.append(Gram(allWords[i], 1))
        elif(len(allWords[i])==2):
            if(inList(bigrams, Gram(allWords[i], 0))):
                bigrams[getIndex(bigrams, Gram(allWords[i], 0))].freq = bigrams[getIndex(bigrams, Gram(allWords[i], 0))].freq + 1
            else:
                bigrams.append(Gram(allWords[i], 1))
        elif(len(allWords[i])==1):
            if(inList(onegrams, Gram(allWords[i], 0))):
                onegrams[getIndex(onegrams, Gram(allWords[i], 0))].freq = onegrams[getIndex(onegrams, Gram(allWords[i], 0))].freq + 1
            else:
                onegrams.append(Gram(allWords[i], 1))
    oneLetterWords = onegrams[:]

    for i in range(len(allWords)):
        word = allWords[i]
        x = 0
        while(x+4<=len(word)):
            if(inList(quadgrams, Gram(word[x:x+4], 0))):
                quadgrams[getIndex(quadgrams, Gram(word[x:x+4], 0))].freq = quadgrams[getIndex(quadgrams, Gram(word[x:x+4], 0))].freq + 1
            else:
                quadgrams.append(Gram(word[x:x+4], 1))
            x+=1
        x = 0
        while(x+3<=len(word)):
            if(inList(trigrams, Gram(word[x:x+3], 0))):
                trigrams[getIndex(trigrams, Gram(word[x:x+3], 0))].freq = trigrams[getIndex(trigrams, Gram(word[x:x+3], 0))].freq + 1
            else:
                trigrams.append(Gram(word[x:x+3], 1))
            x+=1
        x = 0
        while(x+2<=len(word)):
            if(inList(bigrams, Gram(word[x:x+2], 0))):
                if(word[x:x+1]==word[x+1:x+2]):
                    doubles[getIndex(doubles, Gram(word[x:x+2], 0))].freq = doubles[getIndex(doubles, Gram(word[x:x+2], 0))].freq + 1
                bigrams[getIndex(bigrams, Gram(word[x:x+2], 0))].freq = bigrams[getIndex(bigrams, Gram(word[x:x+2], 0))].freq + 1
            else:
                if(word[x:x+1]==word[x+1:x+2]):
                    doubles.append(Gram(word[x:x+2], 1))
                bigrams.append(Gram(word[x:x+2], 1))
            x+=1
        x = 0
        while(x+1<=len(word)):
            if(inList(onegrams, Gram(word[x:x+1], 0))):
                onegrams[getIndex(onegrams, Gram(word[x:x+1], 0))].freq = onegrams[getIndex(onegrams, Gram(word[x:x+1], 0))].freq + 1
            else:
                onegrams.append(Gram(word[x:x+1], 1))
            x+=1


    onegrams = sorted(onegrams, key=operator.attrgetter("freq"))
    onegrams.reverse()
    bigrams = sorted(bigrams, key=operator.attrgetter("freq"))
    bigrams.reverse()
    trigrams = sorted(trigrams, key=operator.attrgetter("freq"))
    trigrams.reverse()
    quadgrams = sorted(quadgrams, key=operator.attrgetter("freq"))
    quadgrams.reverse()
    doubles = sorted(doubles, key=operator.attrgetter("freq"))
    doubles.reverse()
    firstLetter = sorted(firstLetter, key=operator.attrgetter("freq"))
    firstLetter.reverse()
    lastLetter = sorted(lastLetter, key=operator.attrgetter("freq"))
    lastLetter.reverse()
    output = getGuess(onegrams, bigrams, trigrams, quadgrams, doubles, oneLetterWords, firstLetter, lastLetter)
    print(output)
    original_stdout = sys.stdout
    """
    with open('output.txt', 'w') as f:
        sys.stdout = f
        print(output)
        sys.stdout = original_stdout
    """
    #printNodes(sorted(onegrams, key=operator.attrgetter("freq")))

def getClosenessOnes(letter, onegrams, oneLetterWords):
    totalOnes = getTotalOccs(onegrams)
    closeness = []
    mostCommonLetters = "ETAOINSHRDLUCMFWGYPBVKXJQZ"
    letterPercents = [12.575645, 9.085226, 8.000395, 7.591270, 6.920007, 6.903785, 6.340880, 6.236609, 5.959034, 4.317924, 4.057231, 2.841783, 2.575785, 2.560994, 2.350463, 2.224893, 1.982677, 1.900888, 1.795742, 1.535701, 0.981717, 0.739906, 0.179556, 0.145188, 0.117571, 0.079130]
    avgLetterPercent = sum(letterPercents)/26.0
    for y in range(26):
        weight = abs(letterPercents[y]-avgLetterPercent)
        diff = letter.freq - (letterPercents[y]/100)*totalOnes
        score = (diff*diff)/(letterPercents[y]/100)*totalOnes
        #score = score/weight
        closeness.append(Gram(mostCommonLetters[y], score))


    closeness = sorted(closeness, key=operator.attrgetter("freq"))
    for e in range(len(oneLetterWords)):
        if(letter.word==oneLetterWords[e].word):
            closeness[getIndex(closeness, Gram(letter.word, 0))].freq = (closeness[12].freq)*-1
    return closeness

def getClosenessFirstLetter(onegrams, firstLetter, fullCloseness):
    totalFirstLetters = getTotalOccs(firstLetter)
    firstLetters = ["T","O","I","S","W","C","B","P","H","F","M","D","R","E","L","N","A"]
    firstPercents = [16.0,7.6,7.3,6.7,5.5,5.2,4.4,4.3,4.2,4,3.8,3.2,2.8,2.8,2.4,2.3,1.7]
    avgLetterPercent = sum(firstPercents)/17.0
    for x in range(len(firstLetter)):
        closeness = fullCloseness[firstLetter[x].word[0:1]]
        for y in range(len(firstLetters)):
            weight = abs(firstPercents[y]-avgLetterPercent)
            diff = firstLetter[x].freq - (firstPercents[y]/100.0)*totalFirstLetters
            score = (diff*diff)/((firstPercents[y]/100.0)*totalFirstLetters)*(getTotalOccs(onegrams)/totalFirstLetters)*(getTotalOccs(onegrams))*(getTotalOccs(onegrams))
            score = score/weight
            closeness[getIndex(closeness, Gram(firstLetters[y][0:1], 0))].freq = (closeness[getIndex(closeness, Gram(firstLetters[y][0:1], 0))].freq+score)/2
    return fullCloseness

def getClosenessDoubles(onegrams, doubles, fullCloseness):
    totalDoubles = getTotalOccs(doubles)
    doubleLetters = ["LL","SS","EE","OO","TT","FF","PP","RR","MM","CC","NN","DD","GG"]
    doublesPercents = [22.988048, 16.135458, 15.059761, 8.366534, 6.812749, 5.816733, 5.458167, 4.820717, 3.824701, 3.306773, 2.908367, 1.713147, 0.996016]
    avgLetterPercent = sum(doublesPercents)/13.0
    for x in range(len(doubles)):
        closeness = fullCloseness[doubles[x].word[0:1]]
        for y in range(len(doubleLetters)):
            weight = abs(doublesPercents[y]-avgLetterPercent)
            diff = doubles[x].freq - (doublesPercents[y]/100.0)*totalDoubles
            score = (diff*diff)/((doublesPercents[y]/100.0)*totalDoubles)*(getTotalOccs(onegrams)/totalDoubles)*(getTotalOccs(onegrams))*(getTotalOccs(onegrams))*.01
            score = score/weight
            closeness[getIndex(closeness, Gram(doubleLetters[y][0:1], 0))].freq = (closeness[getIndex(closeness, Gram(doubleLetters[y][0:1], 0))].freq+score)/2

    return fullCloseness

def getClosenessBis(onegrams, bigrams, fullCloseness):
    totalTwos = getTotalOccs(bigrams)
    mostCommonBis = ["TH", "HE", "IN", "ER", "AN", "RE", "ND", "ON", "EN", "AT", "OU", "ED", "HA", "TO", "OR", "IT", "IS", "HI", "ES", "NG"]
    biPercents = [3.882543, 3.681391, 2.283899, 2.178042, 2.140460, 1.749394, 1.571977, 1.418244, 1.383239, 1.335523, 1.285484, 1.275779, 1.274742, 1.169655, 1.151094, 1.134891, 1.109877, 1.092302, 1.092301, 1.053385]
    avgLetterPercent = sum(biPercents)/20.0
    for x in range(len(mostCommonBis)):
        weight = abs(biPercents[x]-avgLetterPercent)
        diff = bigrams[x].freq - (biPercents[x]/100)*totalTwos
        score = (diff*diff)/(biPercents[x]/100)*totalTwos*(getTotalOccs(onegrams)/totalTwos)
        score = score/weight
        for key in fullCloseness:
            if(key==bigrams[x].word[0:1]):#finding letter to update score with
                for i in range(26):
                    if(fullCloseness[key][i].word==mostCommonBis[x][0:1]):
                        fullCloseness[key][i].freq = (fullCloseness[key][i].freq + score)/2.0
                        fullCloseness[key] = sorted(fullCloseness[key], key=operator.attrgetter("freq"))
            elif(key==bigrams[x].word[-1]):
                for i in range(26):
                    if(fullCloseness[key][i].word==mostCommonBis[x][-1]):
                        fullCloseness[key][i].freq = (fullCloseness[key][i].freq + score)/2.0
                        fullCloseness[key] = sorted(fullCloseness[key], key=operator.attrgetter("freq"))
    return fullCloseness

def getClosenessTris(onegrams, trigrams, fullCloseness):
    totalTris = getTotalOccs(trigrams)
    mostCommonTris = ["THE", "AND", "ING", "HER", "HAT", "HIS", "THA", "ERE", "FOR", "ENT", "ION", "TER", "WAS", "YOU", "ITH", "VER", "ALL", "WIT", "THI", "TIO"]
    triPercents = [3.508232, 1.593878, 1.147042, 0.822444, 0.650715, 0.596748, 0.593593, 0.560594,  0.555372, 0.530771, 0.506454, 0.461099, 0.460487, 0.437213, 0.431250, 0.430732, 0.422758, 0.397290, 0.394796, 0.378058]
    avgLetterPercent = sum(triPercents)/20.0
    for x in range(len(mostCommonTris)):
        weight = abs(triPercents[x]-avgLetterPercent)
        diff = trigrams[x].freq - (triPercents[x]/100)*totalTris
        score = (diff*diff)/(triPercents[x]/100)*totalTris
        score = score/weight
        for key in fullCloseness:
            if(key==trigrams[x].word[0:1]):#finding letter to update score with
                for i in range(26):
                    if(fullCloseness[key][i].word==mostCommonTris[x][0:1]):
                        fullCloseness[key][i].freq = (fullCloseness[key][i].freq + score)/2.0
                        fullCloseness[key] = sorted(fullCloseness[key], key=operator.attrgetter("freq"))
            elif(key==trigrams[x].word[1:2]):
                for i in range(26):
                    if(fullCloseness[key][i].word==mostCommonTris[x][-1]):
                        fullCloseness[key][i].freq = (fullCloseness[key][i].freq + score)/2.0
                        fullCloseness[key] = sorted(fullCloseness[key], key=operator.attrgetter("freq"))
            elif(key==trigrams[x].word[-1]):
                for i in range(26):
                    if(fullCloseness[key][i].word==mostCommonTris[x][-1]):
                        fullCloseness[key][i].freq = (fullCloseness[key][i].freq + score)/2.0
                        fullCloseness[key] = sorted(fullCloseness[key], key=operator.attrgetter("freq"))
    return fullCloseness

def getClosenessQuads(onegrams, quadgrams, fullCloseness):
    totalTris = getTotalOccs(quadgrams)
    mostCommonTris = ["THAT", "THER", "WITH", "TION", "HERE", "OULD", "IGHT", "HAVE", "HICH", "WHIC", "THIS", "THIN", "THEY", "ATIO", "EVER", "FROM", "OUGH", "WERE", "HING", "MENT"]
    triPercents = [0.761242, 0.604501, 0.573866, 0.551919, 0.374549, 0.369920, 0.309440, 0.290544, 0.284292, 0.283826, 0.276333, 0.270413, 0.262421, 0.262386, 0.260695, 0.258580, 0.253447, 0.231089, 0.229944, 0.223347]
    #avgLetterPercent = sum(triPercents)/20.0
    for x in range(len(mostCommonTris)):
        #weight = triPercents[x]-avgLetterPercent
        diff = quadgrams[x].freq - (triPercents[x]/100)*totalTris
        score = (diff*diff)/(triPercents[x]/100)*totalTris
        #score = score/weight
        for key in fullCloseness:
            if(key==quadgrams[x].word[0:1]):#finding letter to update score with
                for i in range(26):
                    if(fullCloseness[key][i].word==mostCommonTris[x][0:1]):
                        fullCloseness[key][i].freq = (fullCloseness[key][i].freq + score)/2.0
                        fullCloseness[key] = sorted(fullCloseness[key], key=operator.attrgetter("freq"))
            elif(key==quadgrams[x].word[1:2]):
                for i in range(26):
                    if(fullCloseness[key][i].word==mostCommonTris[x][-1]):
                        fullCloseness[key][i].freq = (fullCloseness[key][i].freq + score)/2.0
                        fullCloseness[key] = sorted(fullCloseness[key], key=operator.attrgetter("freq"))
            elif(key==quadgrams[x].word[2:3]):
                for i in range(26):
                    if(fullCloseness[key][i].word==mostCommonTris[x][-1]):
                        fullCloseness[key][i].freq = (fullCloseness[key][i].freq + score)/2.0
                        fullCloseness[key] = sorted(fullCloseness[key], key=operator.attrgetter("freq"))
            elif(key==quadgrams[x].word[-1]):
                for i in range(26):
                    if(fullCloseness[key][i].word==mostCommonTris[x][-1]):
                        fullCloseness[key][i].freq = (fullCloseness[key][i].freq + score)/2.0
                        fullCloseness[key] = sorted(fullCloseness[key], key=operator.attrgetter("freq"))
    return fullCloseness

def generateGuess(fullCloseness, elim):
    letters = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
    #letters = ["E","T","A","O","I","N","S","H","R","D","L","U","C","M","F","W","G","Y","P","B","V","K","X","J","Q","Z"]
    guess = ""
    used = []
    i = 0
    for x in range(26):
        rankings = getRankings(letters[x], fullCloseness)
        if(elim):
            i = 0
            while rankings[i].word in used:
                i+=1
            used.append(rankings[i].word)
        guess += rankings[i].word

    return guess

def getRankings(letter, fullCloseness):
    rankings = []

    for key in fullCloseness:
        for i in range(26):
            if(fullCloseness[key][i].word==letter):
                rankings.append(Gram(key, fullCloseness[key][i].freq))

    return sorted(rankings, key=operator.attrgetter("freq"))

def getGuess(onegrams, bigrams, trigrams, quadgrams, doubles, oneLetterWords, firstLetter, lastLetter):
    mostCommonLetters = "ETAOINSHRDLUCMFWGYPBVKXJQZ"
    fullCloseness = OrderedDict()

    used = []
    guess = ""
    for x in range(26):
        fullCloseness.update({onegrams[x].word:getClosenessOnes(onegrams[x], onegrams, oneLetterWords)})

    #530012484
    fullCloseness = getClosenessFirstLetter(onegrams, firstLetter, fullCloseness)
    fullCloseness = getClosenessDoubles(onegrams, doubles, fullCloseness)
    fullCloseness = getClosenessBis(onegrams, bigrams, fullCloseness)
    fullCloseness = getClosenessTris(onegrams, trigrams, fullCloseness)
    fullCloseness = getClosenessQuads(onegrams, quadgrams, fullCloseness)



    for key in fullCloseness:
        """
        guess = guess + fullCloseness[key][0].word
        print("Letter "+key+" is most likely a "+str((fullCloseness[key][0]).word))

        print("Closeness list for "+key+":")
        printNodes(fullCloseness[key])
        """

    guess = generateGuess(fullCloseness, False)
    correct = 0.0
    accuracy  = 0.0
    for x in range(26):
        if(guess[x:x+1]==mostCommonLetters[x:x+1]):
            correct+=1.0
    if(correct!=0.0):
        accuracy = correct/26.0
    return guess


def getTotalOccs(nodes):
    total = 0
    for x in range(len(nodes)):
        total = total + nodes[x].freq
    return total

def printNodes(nodes):#prints all nodes by coordinates for debug purposes

    for i in range(len(nodes)):
        print("Word: "+str(nodes[i].word)+" Freq: "+str(nodes[i].freq))

def getIndex(nodes, node):#check to see if a node exists in an array
    for i in range(len(nodes)):
        if(node.word==nodes[i].word):
            return i
    return 0

def inList(nodes, node):#check to see if a node exists in an array
    for i in range(len(nodes)):
        if(node.word==nodes[i].word):
            return True
    return False

if __name__ == "__main__":
    main()
