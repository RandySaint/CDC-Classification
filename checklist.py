import pickle
import csv
from SP import SP
#from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords
from nltk.tokenize import TreebankWordTokenizer
from collections import defaultdict
#from indexed.py import IndexedOrderedDict

#d = indexed.IndexedOrderedDict()
d = pickle.load(open("dictionary.pickle","rb"))
words = pickle.load(open("wordlist.pickle","rb"))

stop_words = set(stopwords.words('english'))
stop_words.add("yom")
stop_words.add("yof")
stop_words.add("yo")
stop_words.add("y")
stop_words.add("o")
stop_words.add("m")
stop_words.add("male")
stop_words.add("female")
for i in range(1,100):
    stop_words.add(str(i)+"yom")
    stop_words.add(str(i)+"yof")
    stop_words.add(str(i)+"yo")
    stop_words.add(str(i))

print(words[10000])

pooler = SP(1024)

def known(wordlist):
    "The subset of `words` that appear in the dictionary of WORDS."
    return set(w for w in wordlist if w in words)

def edits1(word):
    "All edits that are one edit away from `word`."
    letters    = 'abcdefghijklmnopqrstuvwxyz_'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)

twt = TreebankWordTokenizer()
notwords = set()

with open('test.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    for line in reader:
        #print(line)
        quote = twt.tokenize(line[0].lower())
        q_list = list(filter(lambda token: token not in stop_words, quote))
        for q in q_list:
            if q not in words:
                notwords.add(q)
                #print(q)
                #print(q,line[0].lower())
                #print(q,quote,q_list)

for t in notwords:
    print(t)
