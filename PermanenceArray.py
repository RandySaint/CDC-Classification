# class for Array of Permanence valueso
import numpy as np
import random

class PermanenceArray(object):
    def __init__(self, size=2048, randpct=0.0, threshold=0.25):
        self.threshold = threshold
        # Input is size and random percent to create connections
        self.size = size
        #print(self.size)
        # PermArray (self.pa) is dictionary of the form (index : permanence)
        #  where 'permanence' is value from 0.0 to 1.0
        #  and 'index' indicates there is a connection from this item to that item of index
        self.pa = {}
        # 'On' SDR is the SDR of bits that are connected above the threshold
        self.on = set()
        for i in range(self.size):
            if random.random() <= randpct: # There is a connection here
                perm = random.random()
                self.pa[i] = perm
                if (perm > self.threshold):
                    self.on.add(i)

    def strengthen(self, inputSDR): # inputSDR is a set()
        # Strengthen Permanence based on inputSDR overlap by factor
        # contributors are cells that were on (inputSDR) that are in this permanence array == active distal connections
        #print("Strengthen:  InputSDR=")
        #inputSDR.pr()
        #print("keys")
        #print(self.pa.keys())
        contributors = set(inputSDR).intersection(set(self.pa.keys()))
        #print("Strengthen:  Contributors=")
        #print(contributors)
        for c in contributors:
            was = self.pa[c]
            self.pa[c] = min(1.0,self.pa[c]+0.1)
            #print(c,was,self.pa[c])
            if (self.pa[c] > self.threshold):
                self.on.add(c)

    def weaken(self, inputSDR):
        # Strengthen Permanence based on inputSDR overlap by factor
        # contributors are cells that were on (inputSDR) that are in this permanence array == active distal connections
        contributors = set(inputSDR).intersection(set(self.pa.keys()))
        #print("weaken:  Contributors=")
        #print(contributors)
        for c in contributors:
            was = self.pa[c]
            self.pa[c] = max(0.0,self.pa[c]-0.1)
            #print(c,was,self.pa[c])
            if (self.pa[c] < self.threshold):
                self.on.discard(c)

    def decay(self):
        # Decay all Permanence
        for c in self.pa.keys():
            self.pa[c] = max(0.0,self.pa[c]-0.001)
            if (self.pa[c] < self.threshold):
                self.on.discard(c)

    def updatePermanence(self, inputSDR):
        # Update Permanence based on inputSDR overlap
        # if we have a connection that's in inputSDR, then strengthen it (increment perm)
        # if we have a connection that's not in inputSDR, then weaken it (decrement perm)
        for idx,perm in self.pa.items():
            # have a permanence here check against input
            # TODO: do we only want to adjust the ones above threshold? This will adjust all whether they're above or below the threshold
            if idx in inputSDR:
                # we have a match, strengthen = default value 0.02
                self.pa[idx] = min(1.0,perm+0.02)
                if (self.pa[idx] > self.threshold):
                    self.on.add(idx)
            else:
                # no match, decrement = default value 1
                self.pa[idx] = max(0.0,perm-0.01)
                if (self.pa[idx] < self.threshold):
                    self.on.discard(idx)

    def updateOn(self):
        for idx,perm in self.pa,items():
            if (perm > self.threshold):
                self.on.add(idx)
            else:
                self.on.discard(idx)


    def countOverlap(self, inputSDR):
        # assumes SDR sizes are the same
        #return self.on.getOverlap(inputSDR)
        return len(self.on.intersection(inputSDR))

    def setThreshold(self, thresh): # thresh in 0.0 to 1.0 range
        # TODO: may need to check thresh for validity
        self.threshold = thresh

#    def pushTo(self, testArray):
#        for i in range(self.size):
#            for j in range(64):
#                if self.pa[i][j] > self.threshold:
#                    testArray[i][j] += 1

    def pr(self):
        print(self.__str__())

    def __str__(self):
        st = ""
        for i in range(self.size):
            if i in self.pa:
                st += str(int(9.9*self.pa[i]))
            else:
                st += "."
        return(st)

if __name__ == "__main__":
    # run test
    #sdr = SDR(size=32)
    #sdr.randomlyInitialize(0.25)
    #sdr.pr()
    test = PermanenceArray(size=32,randpct=0.5, threshold=0.4)
    #test.init(sdr)
    print("25% random weights")
    test.pr()
    print("SDR above threshold ",test.threshold)
    print(test.on)
    inputSDR = set()
    for i in range(2,8):
        inputSDR.add(i)
    for i in range(30):
        test.updatePermanence(inputSDR)
        test.pr()
        print(test.on)
