"""Ising Model in two dimensions"""

import math
import numpy as np
import random as rd


# Ferromagnetic coupling
J = 1
class ising:
    w = np.zeros((17, 2))
    Lx = 0
    Ly = 0
    H = 0
    T = 0
    N = 0
    s = np.empty(1, dtype=np.int8)
    def __init__(self, Lx, Ly, magnetic_field, temperature):
        self.Lx = int(Lx)
        self.Ly = int(Ly)
        self.N = int(Lx*Ly)
        self.H = magnetic_field
        self.T = temperature
        self.s = np.random.choice([-1, 1], size= (Lx, Ly))
        self.computeBoltzmannFactors()
    def getSpinState(self):
        return self.s
    def getW(self):
        return self.w
    def computeBoltzmannFactors(self):
        for i in xrange(0,17,4):
            print i
            self.w[i][0] = math.exp(-(i * J + 2 * self.H) / self.T)
            self.w[i][1] = math.exp(-(i * J - 2 * self.H) / self.T)
    def MetropolisStep(self):
        # Choose a random spin
        i = rd.randint(0, self.Lx-1)
        j = rd.randint(0, self.Ly-1)
        # Find its neighbors using periodic boundary conditions
        iPrev = self.Lx-1 if i == 0 else i-1
        iNext = 0 if i == self.Lx-1 else i+1
        jPrev = self.Ly - 1 if j == 0 else j - 1
        jNext = 0 if j == self.Ly - 1 else j + 1
        # Find sum of neighbors
        sumNeighbors = self.s[iPrev][j] + self.s[iNext][j] + self.s[i][jPrev] + self.s[i][jNext]
        print "sumNeighbors: ", sumNeighbors
        delta_ss = int(2*self.s[i][j]*sumNeighbors)
        print "delta_ss: ", delta_ss
        # ratio of Boltzmann factors
        indexw = 0 if self.s[i][j] == -1 else 1
        ratio = self.w[delta_ss+8][indexw]
        print "ratio: ", ratio
        if rd.random() < ratio:
            self.s[i][j] = -self.s[i][j]
            return True
        else:
            return False
    def thermStep(self, MCStep):
        thermstep = int(0.2*MCStep)
        for i in xrange(thermstep):
            self.OneMonteCarloStepPerSpin()
        mAv, m2Av, eAv, e2Av = 0.0, 0.0, 0.0, 0.0
        for s in xrange(MCStep):
            self.magnetizationPerSpin()
            m = self.magnetizationPerSpin()
            e = self.energyPerSpin()
            mAv += m
            m2Av += m * m
            eAv += e
            e2Av += e*e
            print m, e
        mAv /= MCStep
        m2Av/= MCStep
        eAv/= MCStep
        e2Av /= MCStep
        return mAv, math.sqrt(m2Av - mAv*mAv), eAv,math.sqrt(e2Av - eAv*eAv)
    def OneMonteCarloStepPerSpin(self):
        accepts = 0
        for i in xrange(self.N):
            if self.MetropolisStep():
                accepts+=1
        accepttanceRatio = accepts/self.N
    def magnetizationPerSpin(self):
        sSum = 0
        for i in xrange(self.Lx):
            for j in xrange(self.Ly):
                sSum = self.s[i][j]
        return sSum/ self.N
    def energyPerSpin(self):
        sSum, ssSum = 0,0
        for i in xrange(self.Lx):
            for j in xrange(self.Ly):
                sSum += self.s[i][j]
                iNext = 0 if i == self.Lx - 1 else i + 1
                jNext = 0 if j == self.Ly - 1 else j + 1
                ssSum += self.s[i][j] * (self.s[iNext][j] + self.s[i][jNext])
        return -(J*ssSum + self.H*sSum) / self.N




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





