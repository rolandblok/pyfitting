
import numpy as np
import math
import scipy.optimize

X = 0   # vector array indices
Y = 1

# fit y = C + M x
# y = a,b
# C = cx, cy
# M = m11,m12; m21, m22
# x = x,y
#  REWRITE
# y = A.p
# 
# | a | = | 1 0 x y 0 0 | | cx  |
# | b | = | 0 1 0 0 x y | | cy  |
#                         | m11 |
#                         | m12 |
#                         | m21 |
#                         | m22 |
# 
# https://numpy.org/doc/stable/reference/generated/numpy.linalg.lstsq.html
# 
class MyFitProjection() :
    def __init__(self):
        self.y = []
        self.A = []
        self.solved = False
        pass
    def add_measurement(self, x, y):
        self.y.append(y[X])
        self.y.append(y[Y])
        self.A.append([1, 0, x[X], x[Y], 0,    0])
        self.A.append([0, 1, 0,    0,    x[X], x[Y]])

    def solve(self):
        if len(self.y) > 4:
            self.p = np.linalg.lstsq(self.A, self.y, rcond=None)[0]
            self.C = (self.p[0], self.p[1])
            self.M = [[self.p[2], self.p[3]], [self.p[4], self.p[5]]]
            self.Minv = np.linalg.inv(self.M)
            self.solved = True
            return True
        else:
            return False
    def is_solved(self):
        return self.solved

    def evalX2Y(self, x):
        a = self.C[X] + self.p[2]*x[X] + self.p[3]*x[Y]
        b = self.C[Y] + self.p[4]*x[X] + self.p[5]*x[Y]
        return (a, b)

    def evalY2X(self, y):
        ymc = (y[X] - self.C[X], y[Y] - self.C[Y])
        xx = self.Minv[0][0] * ymc[X] + self.Minv[0][1] * ymc[Y]
        xy = self.Minv[1][0] * ymc[X] + self.Minv[1][1] * ymc[Y]
        return (xx, xy)
    


# ===========================
#  TESTING
# ===========================
if __name__ == '__main__':
    print('test MyFitProjection')
    hex_axis = MyFitProjection()
    hex_axis.add_measurement((  0, 1), (100, 50))
    hex_axis.add_measurement((  1, 0), (150,100))
    hex_axis.add_measurement((  0,-1), (100,150))
    hex_axis.add_measurement(( -1, 0), ( 50,100))
    hex_axis.solve()
    mida=(0,0)
    xy = hex_axis.evalX2Y(mida)
    print('a:{} to x:{}'.format(mida, xy))
    mida = hex_axis.evalY2X(xy)
    print('x:{} to a:{}'.format(xy, mida))

    mida=(1,1)
    xy = hex_axis.evalX2Y(mida)
    print('a:{} to x:{}'.format(mida, xy))
    mida = hex_axis.evalY2X(xy)
    print('x:{} to a:{}'.format(xy, mida))
