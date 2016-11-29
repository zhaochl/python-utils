#!/usr/bin/env python
# coding=utf-8

#相似度计算,inA、inB都是行向量
import numpy as np
from numpy import linalg as la
from numpy import array

#欧式距离
#指在m维空间中两个点之间的真实距离
def euclidSimilar(inA,inB):
    d = la.norm(inA-inB)
    d_norm = 1.0/(1.0+d)
    return d_norm


#皮尔逊相关系数
"""
皮尔逊相关系数，在numpy中可以用线性代数模块linalg中的corrcoef()来计算相关系数（correlation coefficient）。得出结果的取值范围是-1～1，可通过“0.5+0.5*corrcoef()”将其缩放到0～1之间
简单的相关系数的分类
0.8-1.0 极强相关
0.6-0.8 强相关
0.4-0.6 中等程度相关
0.2-0.4 弱相关
0.0-0.2 极弱相关或无相关
"""
def pearsonSimilar(inA,inB):
    if len(inA)<3:
        return 1.0
    return 0.5+0.5*np.corrcoef(inA,inB,rowvar=0)[0][1]


#余弦相似度
def cosSimilar(inA,inB):
    inA=np.mat(inA)
    inB=np.mat(inB)
    num=float(inA*inB.T)
    denom=la.norm(inA)*la.norm(inB)
    return 0.5+0.5*(num/denom)

def calc_sim():
    inA=array([1,2,3])
    inB=array([2,4,6])
    t = euclidSimilar(inA,inB)
    #0.21089672205953397
    print t
    t=pearsonSimilar(inA,inB)
    #1.0
    print t
    t = cosSimilar(inA,inB)
    #1.0
    print t
if __name__=='__main__':
    #calc_sim()
    #inA=array([3,4])
    #测试矩阵的范数，即距离,根号下的平方和
    inA=array([4,5])-array([1,1])
    print inA
    t = la.norm(inA)
    print t


