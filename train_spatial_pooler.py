import pickle
import random
from os import path
from SP import SP

# read dictionary of words and synonyms
words = pickle.load(open("wordlist.pickle","rb"))
synonyms = pickle.load(open("dictionary.pickle","rb"))

#if saved/trained SP exits, then load it
"""
if path.exists("trainedSP.pickle"):
    trainedSP = pickle.load(open("trainedSP.pickle","rb"))
else:
"""
trainedSP = SP(256) # new SP with 80 nodes (probably should be 512-1024)
trainedSP.initialize(2*len(words)) # size of inputs will be ~200,000 (twice number of words)

#this trains the list directly, possibly should shuffle the inputs
for sy in synonyms: # synonyms contains sets of synonyms for each word
    if 10635 in synonyms[sy]: print(sy,synonyms[sy])
    trainedSP.train(synonyms[sy])

telescoped = {51307, 10635, 23}
result = trainedSP.whatValue(trainedSP.test(telescoped))
print(result)
#shuffle
#for idx in random.shuffle(list(range(len(words)))):
    #trainedSP.train(synonyms[words[idx]])

#pickle.dump(trainedSP,open('trainedSP.pickle','wb'),protocol=pickle.HIGHEST_PROTOCOL)
