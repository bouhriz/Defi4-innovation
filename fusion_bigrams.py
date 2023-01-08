# this file is used to merge the corpus_megalite files by creating a new file containing 
# the bigrams and the accumulation of their occurrences

# Abderrahim BOUHRIZ
# Rania BOUAITA

import glob 
import os.path 
import os
import nltk
from nltk.util import bigrams, ngrams

# corpus studied
corpus=[]
# dictionary ((key: value)
dictionary = {}

#Reading files
def readfile(i):
    #Changing the encoding from cp1252 to utf8 and ignore errors
    with open(i, 'r', newline='', encoding='utf-8', errors='ignore') as fp:
        corpus = fp.readlines()
    return corpus

# merge bigrams corpus and increment occurences
def fusionBigrams():
    x = range(len(corpus))
    for n in x:
        for text in corpus[n]:
            bigrams = ngrams(str(text).split(), 3)
            for grams in bigrams:
                bigram = grams[0]+" "+grams[1]
                occurence = grams[2]
                if bigram in dictionary :
                    dictionary[bigram] += int(occurence)
                else :
                    dictionary[bigram] = int(occurence)
                
# make a file of bigrams
def filebigrams():
    with open("bigramfile.txt", "w") as file:
        for key in dictionary:
            occurrence = dictionary[key]
            bigram = key+"\t"+str(occurrence)+"\n"
            file.write(bigram)
            


#Reading files from directory
def listdirectory(path):
    l = glob.glob(path+'/*')
    for i in l: 
        if os.path.isdir(i):
            #Reading files
            listdirectory(i)
        else:
            if os.path.splitext(i)[1] == '.bi':
                corpus.append(readfile(i))
            else: print ('extension not handled')



def main():
    listdirectory("Ressources/MEGALITE_FRANCAIS_bi")
    fusionBigrams()
    filebigrams()

main()



