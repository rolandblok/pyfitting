
import numpy as np
import math
from scipy.optimize import curve_fit


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

def myProjection(x_coor,cx,cy,m11,m12,m21,m22):
    y_coors = []
    for x,y in x_coor:
        y_coors.append(cx + m11*x + m12 * y)
        y_coors.append(cy + m21*x + m22 * y)
    return y_coors


class MyFitProjection() :
    def __init__(self):
        self.y = []
        self.x = []
        self.A = []
        self.solved = False
        pass
    def add_measurement(self, x, y):
        self.x.append(x)
        self.y.append(y[X])
        self.y.append(y[Y])
        self.A.append([1, 0, x[X], x[Y], 0,    0])
        self.A.append([0, 1, 0,    0,    x[X], x[Y]])

    def solveLSQ(self):
        if len(self.y) > 4:
            self.p = np.linalg.lstsq(self.A, self.y, rcond=None)[0]
            self.C = (self.p[0], self.p[1])
            self.M = [[self.p[2], self.p[3]], [self.p[4], self.p[5]]]
            self.Minv = np.linalg.inv(self.M)
            return True
        else:
            return False

    def solveOptimize(self):
        if len(self.y) > 4:
            self.p = curve_fit(myProjection,self.x,  self.y)[0]
            self.C = (self.p[0], self.p[1])
            self.M = [[self.p[2], self.p[3]], [self.p[4], self.p[5]]]
            self.Minv = np.linalg.inv(self.M)
            return True
        else:
            return False


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
    hex_axis_lsq = MyFitProjection()
    hex_axis_lsq.add_measurement([  0, 1], (100, 50))
    hex_axis_lsq.add_measurement([  1, 0], (150,100))
    hex_axis_lsq.add_measurement([  0,-1], (100,150))
    hex_axis_lsq.add_measurement([ -1, 0], ( 50,100))
    hex_axis_lsq.solveLSQ()
    hex_axis_opt = MyFitProjection()
    hex_axis_opt.add_measurement([  0, 1], (100, 50))
    hex_axis_opt.add_measurement([  1, 0], (150,100))
    hex_axis_opt.add_measurement([  0,-1], (100,150))
    hex_axis_opt.add_measurement([ -1, 0], ( 50,100))
    hex_axis_opt.solveOptimize()


    mida=(0,0)
    xy = hex_axis_lsq.evalX2Y(mida)
    print('lsq : a:{} to x:{}'.format(mida, xy))
    xy = hex_axis_opt.evalX2Y(mida)
    print('opt : a:{} to x:{}'.format(mida, xy))
 
    mida = hex_axis_lsq.evalY2X(xy)
    print('lsq : x:{} to a:{}'.format(xy, mida))
    mida = hex_axis_opt.evalY2X(xy)
    print('opt : x:{} to a:{}'.format(xy, mida))

    mida=(1,1)
    xy = hex_axis_lsq.evalX2Y(mida)
    print('lsq : a:{} to x:{}'.format(mida, xy))
    xy = hex_axis_opt.evalX2Y(mida)
    print('opt : a:{} to x:{}'.format(mida, xy))


    mida = hex_axis_lsq.evalY2X(xy)
    print('lsq : x:{} to a:{}'.format(xy, mida))
    mida = hex_axis_opt.evalY2X(xy)
    print('opt : x:{} to a:{}'.format(xy, mida))
