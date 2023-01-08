# Bigrams language model baseline sentence generator (ML-2)
# Marcov's algorithm for producing sentences from a starting word based on probabilities

# Abderrahim BOUHRIZ
# Rania BOUAITA


import numpy as np
import sys
np.set_printoptions(threshold=sys.maxsize)

# open the corpus
def openfile():
    file = open("testfile.txt", "r")
    corpus = file.read().split("\n")
    corpus = [corpus]
    return corpus


# get bigrams from the corpus without occurrences
def getBigrams(corpus):
    Bigrams = []
    for bigram in corpus[0]:
        bigram = bigram.split("\t")
        Bigrams = np.append(Bigrams,bigram[0])
    return Bigrams


# get successors from bigrams without occurrences
def getSuccessors(Bigrammes):
    successors=[]
    for bigram in Bigrammes:
        unigram = bigram.split(" ")
        successors = np.append(successors,unigram[0]) # get the first word
        successors = np.append(successors,unigram[1]) # get the second word
    successors = list(dict.fromkeys(successors)) # remove repetitive words
    return successors


# get the number of occurrences of a given bigram
def getNumberOfOccurence(bigram):
    bigramOccurence = makeDictFromCorpus()
    if bigram not in bigramOccurence.keys():
        return 0
    return bigramOccurence[bigram]

# make a dictionary from a corpus
def makeDictFromCorpus():
    bigramOccurence ={}
    corpus=openfile()
    for i in corpus[0]:
        elements = i.split("\t")
        bigramOccurence[elements[0]] = elements[1]
    return bigramOccurence


# get unigrams from bigrams with the occurrences of each bigram
def getUnigramsFromBigrams():
    unigramsOccurence = {}
    bigramsOccurence = makeDictFromCorpus()
    for k, v in bigramsOccurence.items():
        elements = k.split(" ")
        if elements[0] in unigramsOccurence.keys():
            unigramsOccurence[elements[0]] += int(v)
        else:
            unigramsOccurence[elements[0]] = int(v)

        if elements[1] in unigramsOccurence.keys():
            unigramsOccurence[elements[1]] += int(v)
        else:
            unigramsOccurence[elements[1]] = int(v)
    return unigramsOccurence


# create a matrix based on the probabilities of the Markov chain 
# A Markov chain is a model that describes a sequence of possible events in which
# the probability of each event depends only on the state reached in the previous event.
def makeMatrix(Bigrams,successors):
    size_x = len(Bigrams) # the bigrams are rows of the matrix
    size_y = len(successors) # the successors are columns of the matrix
    matrix = np.zeros((size_x,size_y))
    for i in range(size_x):
        for j in range(size_y):
            mot_big = Bigrams[i].split(" ") 
            condidat= mot_big[1]+" "+successors[j] # concatenate the second word of the bigram with its successor
            occurenceOfBigram=getNumberOfOccurence(condidat) # count the number of occurrences of word(t) after word(t-1)
            if(int(occurenceOfBigram) == 0): # avoid division on zero
                matrix[i][j] = 0
            else:
                occurenceOfUnigram=getUnigramsFromBigrams()[mot_big[1]]
                #calculate the probability (the number of occurrences of bigram on the number of occurrences of successor)
                matrix[i][j] = int(occurenceOfBigram) / int(occurenceOfUnigram)
    return matrix


# Get the bigram index of the matrix from the given word
def getBigramIndexFromMatrix(word):
    indices = []
    bigramsOccurence = makeDictFromCorpus()
    unigramsOccurence = []
    for k in bigramsOccurence.keys():
        elements = k.split(" ")
        unigramsOccurence = np.append(unigramsOccurence,elements[1])
    for i in range(len(unigramsOccurence)):
        if(word ==unigramsOccurence[i]):
            indices.append(i)
    return indices


# Get the successor index of the given word based on the row of the matrix that has the maximum value.
def getSuccessorIndexFromSuccessors(matrix,i,successors):
    max= 0
    for j in range(len(successors)):
        if(matrix[i][j]>=max):
            max = matrix[i][j]
            indexJ = j
    return indexJ


# from the indices i and j, we predict the next word of a given word
def makeSentence(successors,matrix,word,size):
    sentence = word;
    for k in range(int(size)-1):
            i = getBigramIndexFromMatrix(word)
            j = getSuccessorIndexFromSuccessors(matrix,i[0],successors)
            sentence += " " + successors[j]
            word = successors[j]
    return sentence


# menu where we call the function that generates the sentence
def menu(successors,matrix):
    while True:
        word = input("Enter the start word: ");
        size = input("Choose the size of the sentence (5, 10, 15): ")
        sentence = makeSentence(successors,matrix,word,size)
        print(sentence)



# main program
def main():
    corpus = openfile()
    bigrams = getBigrams(corpus)
    successors = getSuccessors(bigrams)
    matrix = makeMatrix(bigrams, successors)
    menu(successors,matrix)
main()