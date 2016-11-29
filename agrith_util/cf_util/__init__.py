#!/usr/bin/python
# -*- coding: utf-8 -*-
from math import *

"""
计算两个dict 向量的余弦相似度
cosine(a,b) = a*b / |a|*|b| =x / y
demo:
d1 = {'A':1,'B':2}
d2 = {'B':2,'C':1}
sim = calcCosine(d1,d2) ##0.8
"""
def calcCosine(dict1,dict2):

    x=0.0
    y=0.0
    y1=0.0
    y2=0.0
    for k1,v1 in dict1.viewitems():
        y1 += pow(v1,2)
        print '--',k1,v1,y1
    for k2,v2 in dict2.viewitems():
        y2 += pow(v2,2)

    for k2,v2 in dict2.viewitems():
        print '==',k2,v2,y2
        # a1*b1+a2*b2.. 自动补全计算集合
        if dict1.has_key(k2):
            x+= v2* dict1[k2]
    print '**',x,y1,y2
    y = sqrt(y1) * sqrt(y2)
    return  x/y

if __name__ == '__main__':
    #sim = 2/sqrt(4)
    #print 'hello',sim

    d1 = {'A':1,'B':2}
    d2 = {'B':2,'C':1}
    c1 = {12994L: 0, 10436L: 0, 14471L: 5, 15080L: 0, 10538L: 0, 14220L: 0, 14933L: 0, 10553L: 0, 12506L: 0}
    c2= {7808L: 5, 4980L: 0, 10964L: 5}
    sim = calcCosine(d1,d2) ##0.894427191
    print sim
    sim = calcCosine(c1,c2) ##0.894427191
    print sim