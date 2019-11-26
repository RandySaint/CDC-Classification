#Spatial Pooler
from SDR import SDR
from PA import PA
import numpy as np
import random

class SP(object):
    def __init__(self, size=1024):
        # initialize basic stuff here
        # size is number of cells(minicolumns) represented
        self.size = size
        self.columns = SDR(size)

    def initialize(self, inputSize):
        # inputSize - number of bits in the input - will be encoded external to the SP
        # each cell in SP gets a connection matrix to the Input(s)
        self.inputSize = inputSize
        # dynamically create an SDR for each column with random connections to 25% of the inputs
        # pa is the permanence of each of the connections to the inputs
        self.pa = [PA(size=self.inputSize,randpct=0.25) for i in range(self.size)]
        # create an array for adding boost - randomize?
        self.boost = np.zeros((self.size))
        # TODO: Should we initialize boost to non-zero values?
        #self.inputSDR = SDR(self.inputCount)

    def test(self, inputSDR):
        # inputSDR is array of encoded bits
        #inputSDR = SDR(self.inputSize, inputValues)
        # create an array for summations
        sums = np.zeros((self.size))
        # for each cell check overlapp of permanence array
        for i in range(self.size):
            # could factor (divide) boost here
            sums[i] = self.pa[i].countOverlap(inputSDR) + self.boost[i]
            #arr[i][j] = self.pa[i][j].checkOverlap(inputSDR)
            self.boost[i] += 0.05 # (Tunable)
        # find cutoff for top 2-4% (tunable?)
        threepct = int(0.03 * float(self.size)) #  3%
        threepct = - threepct
        #ind = np.argpartition(a, -4)[-4:]
        # indices should have an array of indices (count=top 3%) that are the highest sums
        indices = np.argpartition(sums, threepct)[threepct:]
        # create output SDR with summations that exceed cutoff
        ret = set(indices)
        return ret # the on bits of the SP

    def train(self, inputSDR):
        ret = self.test(inputSDR)
        for ind in ret:
            self.boost[ind] = 0.0
            self.pa[ind].updatePermanence(inputSDR)
        return ret # the on bits of the SP

    def whatValue(self, testSDR):
        # gets is list of indexes of which values to get
        # return array of values
        # build an testInput SDR by reverse engineering
        print ("whatValue")
        # create an empty testInput
        countDict = {}
        # for each on bit in the testSDR, increment the values in TestInput that correspond to the permanence>threshold inputs
        for i in testSDR: #(it's a set of on indexes)
            for j in self.pa[i].on:
                if j in countDict:
                    countDict[j] = countDict[j]+1
                else:
                    countDict[j] = 1
        maxi = 0
        ret = set()
        for i in countDict:
            if countDict[i] > maxi: maxi = countDict[i]
            print ("countDict["+ str(i) +"]="+str(countDict[i]))
        print(maxi)
        maxi = maxi
        for i in countDict:
            if countDict[i] == maxi: ret.add(i)
        return ret



    def prPA(self, i):
        self.pa[i].pr()


    #def feedforward(inputs):
        # should

if __name__ == "__main__":
    # run test
    test = SP(100) # internally 100 cells
    test.initialize(400) # input has 400 bits

    inp = {4,100,260,310}
    save = test.train(inp)
    put = test.train(inp)
    print(put)
    print("")
    for j in range(100):
        put = test.train(inp)
        print(j)
        #print(put)
        #for k in put: print(k," ",test.pa[k])
        #print("")
        for i in range(100):
            a = random.uniform(0,400)
            b = random.uniform(0,400)
            c = random.uniform(0,400)
            d = random.uniform(0,400)
            out = test.train({a,b,c,d})
            #print ("")
            #test.inputSDR.pr()
            #if a == 4 and b==1 and c==6 and d == 10:
            #    out.pr()

    out = test.test(inp)
    print ("final out ",inp)
    print(out)
    print ("first out ", inp)
    print(save)
    out = test.test(inp)
    print ("final out ",inp)
    print(out)
    print(test.whatValue(out))
