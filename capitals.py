import pickle
#from nltk.corpus import wordnet as wn
from collections import defaultdict
#from indexed.py import IndexedOrderedDict

#d = indexed.IndexedOrderedDict()
words = pickle.load(open("wordlist.pickle","rb"))

print(len(words))
print(words[10000])

cap = []

for idx,w in enumerate(words):
    if (w.lower()!=w):
        #print("word["+str(idx)+"]="+words[idx])
        cap.append(w)

print(len(cap))
