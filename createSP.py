import pickle
from numpy.random import permutation
from SP import SP
#from nltk.corpus import wordnet as wn
from collections import defaultdict
#from indexed.py import IndexedOrderedDict

#d = indexed.IndexedOrderedDict()
d = pickle.load(open("dictionary.pickle","rb"))
words = pickle.load(open("wordlist.pickle","rb"))

print(len(words))
print(words[10000])

pooler = SP(100)

pooler.initialize(2*len(words))

for idx in permutation(len(words)):
    print("word["+str(idx)+"]="+words[idx]," thesaurus=",d[words[idx]])


