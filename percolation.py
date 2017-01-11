import math
import numpy as np
import random as rd

class percolation:
    N = 20
    p = 0.55
    occupied = np.zeros((1,2), dtype=np.bool_)
    clusters = 0
    label = np.zeros((), dtype=np.int8)
    currentLabel = 0
    spanningLabel = 0
    def __init__(self):
        pass
    def addNewNeighboer(self,i, j):
        if self.occupied[i][j] and self.label[i][j] == 0:
            # site is occupied and not yet labeled
            self.label[i][j] = self.currentLabel
            if i <self.N-1:
                self.addNewNeighboer(i+1, j)
            if i >0:
                self.addNewNeighboer(i-1, j)
            if j<self.N-1:
                self.addNewNeighboer(i, j+1)
            if j>0:
                self.addNewNeighboer(i, j-1)
    def newSample(self):
        for i in xrange(self.N):
            for j in xrange(i, self.N):
                self.occupied[i][j] = rd.random < self.p
                self.label[i][j] = 0
        # find and label all clusters of occupied sites
        self.clusters = 0
        for i in xrange(self.N):
                for i in xrange(self.N):
                    if self.occupied[i][j] and self.label[i][j] == 0:
                        self.currentLabel += self.clusters
                        """assign a new label"""
                        self.addNewNeighboer(i, j)
        # check each cluster for percolation
        self.spanningLabel = 0
        for cluster in xrange(1, self.clusters+1):
            # check west boundary sites
            west = False
            for j in xrange(self.N):
                if self.label[0][j] == cluster:
                    west = True
                    break
            east = False
            for j in xrange(self.N):
                if self.label[0][j] == cluster:
                    east = True
                    break
            south = False
            for j in xrange(self.N):
                if self.label[0][j] == cluster:
                    south = True
                    break
            north = False
            for j in xrange(self.N):
                if self.label[0][j] == cluster:
                    north = True
                    break
            if west and east and south and north:
                self.spanningLabel = cluster
                break
