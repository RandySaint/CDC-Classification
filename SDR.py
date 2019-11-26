# Class for SDR data structure (List Based)
# SDR will be stored as a 1 dimensional list of numbers, indicating where bits are set to 1

import numpy as np
import random

class SDR(object):
    def __init__(self, size=1, pct=0.0, meta={}):
        self.size = size
        self.sdr = set()
        self.meta = meta
        if pct > 0.0:
            self.randomlyInitialize(pct)

    def initialize(self, inputList):
        # inputList is list of bits toset
        self.sdr.clear()
        for pos in inputList:
            self.sdr.add(pos)

    def randomlyInitialize(self, pct=0.5):
        # randomly set pct bits
        for i in range(self.size):
            if random.random() <= pct:
                self.setBit(i)

    def getBit(self, pos):
        # get the bit state at pos
        # pos should be < size
        # if the pos value is in the list
        if pos in self.sdr:
            return True
        return False

    def setBit(self, pos):
        # simply add this pos to the list
        # pos should be < size
        self.sdr.add(pos)

    def clearBit(self, pos):
        # pos must be < size
        self.sdr.discard(pos)

    def clear(self):
        self.sdr.clear()

    def getAll(self):
        # col must be < 64
        return self.sdr

    def append(self, sdr, offset=0):
        # if (sdr.getSize() + offset) > self.sdr.size: Error or grow this?
        for pos in sdr.getAll():
            self.sdr.add(pos+offset)

    def getSize(self):
        return self.size

    def getOverlap(self, other):
        # if sizes different, fail
        return len(self.sdr.intersection(other.sdr))

    def merge(self, other):
        # merge 2 SDRs and return new SDR
        return self.sdr.union(other.sdr)

    def pr(self):
        # print self.meta
        print(self.__str__())

    def __str__(self):
        st = ""
        for i in range(self.size):
            if self.getBit(i):
                st += "1"
            else:
                st += "."
        return(st)


if __name__ == "__main__":
    # run test
    #w = random.randint(1,32)
    w = 32
    print(w)
    test = SDR(size=w)
    test.pr()
    c = random.randint(0,w-1)
    print("Bit",c)
    test.setBit(c)
    test.pr()
    print ("Overlap=", test.getOverlap(test))
    test.clearBit(c)
    test.pr()
    print("Random(0.2)")
    test.randomlyInitialize(0.2)
    test.pr()
    print ("Overlap=", test.getOverlap(test))
    a1 = SDR(size=16)
    a1.randomlyInitialize(0.2)
    print("A1")
    a1.pr()
    a2 = SDR(size=16)
    a2.randomlyInitialize(0.2)
    print("A2")
    a2.pr()
    test.clear()
    test.append(a1)
    test.append(a2,16)
    print("Combined")
    test.pr()
    newlist = [1,2,3,4]
    test.initialize(newlist)
    test.pr()
