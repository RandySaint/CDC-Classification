import pickle
from nltk.corpus import wordnet as wn
#from nltk.corpus import stopwords
from collections import defaultdict
#from indexed.py import IndexedOrderedDict

#d = indexed.IndexedOrderedDict()
d = defaultdict(list)
words = []

#stop_words = set(stopwords.words('english'))

for nw in wn.all_synsets():
    for n in nw.lemma_names():
        words.append(n)

print("num synsets:", len(words))
for s in words:
    if (s.lower()==s):
        d[s] = []
words = list(d)
print("num words:", len(words))

for s in words:
    for syn in wn.synsets(s):
        for l in syn.lemma_names():
            if l in words:
                g = words.index(l)
                if g not in d[s]:
                    d[s].append(g)
    print(s,", index:",words.index(s))
    print(d[s])
    a = []
    for w in d[s]:
        a.append(words[w])
    print(a)

filehandler = open('dictionary.pickle', 'wb')
pickle.dump(d,filehandler,protocol=pickle.HIGHEST_PROTOCOL)

listfilehandler = open('wordlist.pickle', 'wb')
pickle.dump(words, listfilehandler, protocol=pickle.HIGHEST_PROTOCOL)

