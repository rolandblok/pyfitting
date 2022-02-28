
import random
import numpy as np
from matplotlib import pyplot as plt
import math
from scipy.optimize import curve_fit



# fit y = C + M x
#  y = a
#  C = cx
#  M = m11
#  x = x
#  REWRITE
#  y = A.p
# 
# | a | = | 1 x | | cx  |
#                 | m11 |
# 
# https://numpy.org/doc/stable/reference/generated/numpy.linalg.lstsq.html
# https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.curve_fit.html


def myLine(x,c,m):
    return c + m*x

def myLineInv(y,c,m):
    return (y-c)/m

class myLineObj:
    def __init__(self, const, scale):
        self.C = const
        self.M = scale    
    def eval(self, x) :
        return myLine(x, self.C, self.M)



class MySolvers() :
    def __init__(self):
        self.y = []
        self.x = []
        self.A = []
        self.solved = False
        pass
    def add_measurement(self, x, y):
        self.x.append(x)
        self.y.append(y)
        self.A.append([1, x])

    def solveLSQ(self):
        if len(self.y) > 2:
            self.p = np.linalg.lstsq(self.A, self.y, rcond=None)[0]
            self.C = self.p[0]
            self.M = self.p[1]
            self.solved = True
            return True
        else:
            return False


    def solveOptimize(self):
        if len(self.y) > 2:
            self.p = curve_fit(myLine, self.x,  self.y)[0]
            self.C = self.p[0]
            self.M = self.p[1]
            self.solved = True
            return True
        else:
            return False

    def evalX2Y(self, x):
        a = myLine(x, self.C, self.M)
        return a

    def evalY2X(self, y):
        x = myLineInv(y,self.C, self.M)
        return x





# ===========================
#  TESTING
# ===========================
if __name__ == '__main__':
    print('test MyFitProjection')
    lsq_line = MySolvers()
    opt_line = MySolvers()
    my_line  = myLineObj(2,3)
    
    x = range(-4,6,1)
    y = []
    for xe in x:
        r =  2* random.random()
        ye = my_line.eval(xe) + r
        lsq_line.add_measurement( xe, ye)
        opt_line.add_measurement( xe, ye)
        y.append(ye)
    plt.plot(x,y, "ob")
    
    lsq_line.solveLSQ()
    opt_line.solveOptimize()

    xs= np.arange(-5,6,1)
    ylsq = lsq_line.evalX2Y(xs)
    yopt = opt_line.evalX2Y(xs)

    plt.plot(xs,ylsq, "-r")
    plt.plot(xs,yopt, "-g")
    plt.show()

