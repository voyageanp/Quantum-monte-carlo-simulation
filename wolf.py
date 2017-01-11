import math
import numpy as np
import random as rd
from collections import deque

# Ferromagnetic coupling

class wolf:
    w = np.zeros((17, 2))
    J = 1
    Lx = 0
    Ly = 0
    H = 0
    T = 0
    N = 0
    s = np.empty(1, dtype=np.int8)
    cluster = np.empty()
    addProbability = 0

    """variables to measute chi and its error estimate"""
    chi = 0
    # current susceptibility per spin
    chiSum = 0
    # accumulate chi values
    chiSqdSum = 0
    # accumulate chi^2 values
    nChi =0
    # number of values accumulated
    """variables to measue autocorrelation time"""
    nSave = 10
    # number of values to save
    cChiSum = 0
    # accumulate
    chiSave = deque()
    # saved values
    cChi= np.empty()
    # correlation sums
    nCorr = 0
    # number of values accumalated
    """variables to estimate fluctuations by blocking"""
    stepPerBlock =1000
    # suggested in wolff paper
    chiBlock =0.0
    # used to calculate block average
    chiBlockSum=0.0
    # accumalate block <chi> values
    chiBlockSqdSum=0.0
    # accumulate block <chi>^2 values
    stepInBlock=0
    # number of steps in current block
    blocks =0
    def __init__(self, Lx, Ly, magnetic_field, temperature):
        self.Lx = int(Lx)
        self.Ly = int(Ly)
        self.N = int(Lx*Ly)
        self.H = magnetic_field
        self.T = temperature
        self.s = np.random.choice([-1, 1], size= (Lx, Ly))
        self.cluster = np.zeros((Lx, Ly), dtype=np.bool_)
        self.addProbability = 1-math.exp(-2*self.J/temperature)
        """Initiate observable"""
        self.cChi = np.zeros(self.nSave+1, dtype=np.int)

    def getSpinState(self):
        return self.s
    def getW(self):
        return self.w
    def MetropolisStep(self):
        # Choose a random spin
        i = rd.randint(0, self.Lx-1)
        j = rd.randint(0, self.Ly-1)
        self.growCluster(i, j, self.s[i][j])
    def growCluster(self, i, j, clusterSpin):
        self.cluster[i][j] = True
        self.s[i][j] *=-1
        iPrev = self.Lx - 1 if i == 0 else i - 1
        iNext = 0 if i == self.Lx - 1 else i + 1
        jPrev = self.Ly - 1 if j == 0 else j - 1
        jNext = 0 if j == self.Ly - 1 else j + 1
        # // if the neighbor spin does not belong to cluster, then try to add it to the cluster
        if not self.cluster[iPrev][j]:
            self.tryAdd(iPrev, j, clusterSpin)
        if not self.cluster[iNext][j]:
            self.tryAdd(iNext, j, clusterSpin)
        if not self.cluster[i][jPrev]:
            self.tryAdd(i, jPrev, clusterSpin)
        if not self.cluster[iPrev][j]:
            self.tryAdd(iPrev, j, clusterSpin)
    def tryAdd(self, i, j, clusterSpin):
        if self.s[i][j] == clusterSpin:
            if rd.random < self.addProbability:
                self.growCluster(i, j, clusterSpin)

    def measureObsevables(self):
        # observables are derived from the magnetic moment
        M = 0
        for i in xrange(self.Lx):
            for j in xrange(self.Ly):
                M += self.s[i][j]
        chi = M * float(M)/self.N
        # accumulate values
        self.chiSum += self.chi
        self.chiSqdSum += self.chi * self.chi
        self.nChi+=1

        # accumulate correlation values
        if (self.chiSave.size() == self.nSave):
            self.cChiSum += self.chi
            self.cChi[0] += self.chi * self.chi
            self.nCorr+=1
            it = iter(self.chiSave)
            it.next()
            for i in xrange(self.nSave):
                self.cChi[i] += it * self.chi;
                try:
                    it.next()
                except StopIteration:
                    print "StopIteration"
                self.chiSave.pop(0)
                # remove oldest saved chi value
            self.chiSave.push_front(chi)
            # add current chi value
        #accumulate block values
        self.chiBlock += self.chi;
        self.stepInBlock+=1
        if self.stepInBlock == self.stepsPerBlock:
            self.chiBlock /= self.stepInBlock;
            self.chiBlockSum += self.chiBlock;
            self.chiBlockSqdSum += self.chiBlock * self.chiBlock;
            self.blocks+=1
            stepInBlock = 0;
            chiBlock = 0;
    def computeAverages(self):
        """double chiAve;               // average susceptibility per spin
double chiError;             // Monte Carlo error estimate
double chiStdDev;            // Standard deviation error from blocking
double tauChi;               // autocorrelation time
double tauEffective;         // effective autocorrelation time"""
        #average susceptibility per spin
        chiAve = self.chiSum / self.nChi
        """Monte Carlo error estimate"""
        chiError = math.sqrt(self.chiSqdSum / self.nChi - self.chiAve * self.chiAve);
        chiError /= math.sqrt(float(self.nChi))
        """exponential correlation time"""
        tauChi = 0
        cAve = self.cChiSum / self.nCorr
        c0 = self.cChi[0] / self.nCorr - cAve * cAve
        for i in xrange(self.nSave):
            c = (self.cChi[i] / self.nCorr - cAve * cAve) / c0
            if (c > 0.01) :
                tauChi += -i / math.log(c);
            else:
                tauChi /= (i - 1);
                break
            if i == self.nSave:
                tauChi /= self.nSave;
        """standard deviation from blocking"""
        chiBlockAve = self.chiBlockSum / self.blocks
        chiStdDev = chiBlockSqdSum / blocks
        chiStdDev = math.sqrt(chiStdDev - chiBlockAve * chiBlockAve)
        chiStdDev /= math.sqrt(float(blocks))
        """effective autocorrelation time"""
        tauEffective = chiStdDev / chiError
        tauEffective *= tauEffective / 2


if __name__ == '__main__':
    print "Two-dimesional Ising Model "
    Lx = 10
    Ly = 10
    H =5
    T = 10
    model = ising(Lx, Ly, H, T)
    # print model.getW()
    a, b, c, d= model.thermStep(30)
    print a, b
    print c, d





