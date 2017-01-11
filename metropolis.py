import math
import numpy as np
import random as rd

def P(x):
    return math.exp(-x * x / 2)/ math.sqrt(2*math.pi)
def f_over_w(x):
    return x*x
class metropolis:
    x = 0 #"Initial position of walker"
    delta=1.0 #" Step size"
    accepts = 0 #" Number of steps accepted"
    sum = 0
    sqdSum = 0
    errSum = 0
    def MetroplisStep(self):
        xTrial = self.x+(2*rd.random() -1)*self.delta
        w = P(xTrial)/ P(self.x)
        if (w >=1):
            self.x = xTrial #"uphill so accept the step"
            self.accepts +=1
        else:
            if (rd.random() < w):
                self.x = xTrial
                self.accepts += 1
    def trial(self, M, N):
        for i in xrange(int(M)):
            avg =0.0
            var = 0.0
            for j in xrange(int(N)):
                self.MetroplisStep()
                fx = f_over_w(self.x)
                avg +=fx
                var +=fx*fx
            avg /= (N)
            var /= (N)
            var = var - avg*avg
            err = math.sqrt(var/(N))
            self.sum += avg
            self.sqdSum += avg *avg
            self.errSum += err
        ans = self.sum / M
        stdDev = math.sqrt(self.sqdSum/ M - ans*ans)
        err = self.errSum / M
        err /= math.sqrt(float(M))
        return ans, stdDev, err, self.accepts / (N*M)

if __name__ == '__main__':
    # size = raw_input('Enter step size: ')
    trial = float(raw_input('Enter number of trials: '))
    N = float(raw_input('Enter steps per trial: '))
    mt = metropolis()
    ans, sD, err, ratio = mt.trial(trial, N)
    print ans, sD, err, ratio