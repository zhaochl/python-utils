#!/usr/bin/env python
# coding=utf-8
import numpy as np

import matplotlib
matplotlib.use('Agg')

from matplotlib.pyplot import plot,savefig
def sin_x():
    x=np.linspace(-4,4,30)
    y=np.sin(x);

    plot(x,y,'--*b')

    savefig('static/sin.jpg')

def yx():
    x = [0, 1,2,3,4]
    y = [0, 1,2,3,4]  # y = x

    plot(x, y)
    savefig("static/yx.jpeg")

def x2():
    x2 = range(0,10)
    y2 = range(0,10)  # y = x
    x1 = range(0, 10)
    y1 = [num**2 for num in x1] # y = x^2
    plot(x1, y1, x2, y2)
    savefig("static/x2.jpeg")

if __name__=='__main__':
    #draw()
    #sin_x()
    yx()
    x2()
