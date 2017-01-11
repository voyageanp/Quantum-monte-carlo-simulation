import numpy as np
import math as mt
import random

class md:
    N = 64  # Number of particles
    r = np.zeros((N, 3))  # positions
    v = np.zeros((N, 3))  # velocities
    a = np.zeros((N, 3))  # accelerations
    L = 10
    vMax = 0.1
    def __init__(self):
        n = int(mt.ceil(mt.pow(self.N, 1.0/3)))
        a = self.L / n
        p =0
        for x in xrange(n):
            for y in xrange(n):
                for z in xrange(n):
                    if (p<self.N):
                        self.r[p][0] = (x + 0.5) *a
                        self.r[p][1] = (y + 0.5) * a
                        self.r[p][2] = (z + 0.5) * a
                    p+=1
        for x in xrange(self.N):
            for i in xrange(3):
                self.v[x][i] = self.vMax * (2 * random.random() -1)
    def Accelerations(self):
        """Already accelerations is initialized as 0 for every component"""
        for i in xrange(self.N-1):
            for j in xrange(i+1, self.N):
                rij = np.zeros(3)
                rSpd = 0
                for k in xrange(3):
                    rij[k] = self.r[i][k] - self.r[j][k]
                    rSpd += rij[k] * rij[k]
                f = 24*(2* mt.pow(rSpd, -7) - mt.pow(rSpd, -4))
                for k in xrange(3):
                    self.a[i][k] += rij[k] * f
                    self.a[j][k] -= rij[k] * f
        return  self.a
    def velocityVerlet(self, dt):
        self.Accelerations()
        for i in xrange(self.N):
            for j in xrange(3):
                self.r[i][j] += self.v[i][j] *dt + 0.5 *self.a[i][j] *dt*dt
                self.v[i][j] += 0.5*self.a[i][j] *dt
        self.Accelerations()
        for i in xrange(self.N):
            for j in xrange(3):
                self.v[i][j] += 0.5 *self.a[i][j] *dt
    def instantaneousTemperature(self):
        from numpy import linalg as LA
        return LA.norm(self.v) / (3*(self.N -1))
if __name__ == '__main__':
    md = md()
    dt = 0.01
    for mainl in xrange(1000):
        md.velocityVerlet(dt)
        print md.instantaneousTemperature()



