#!/usr/bin/env python
# coding=utf-8
from pdb import *

from numpy import *
from numpy import linalg as la
"""
奇异值分解（Singular Value Decomposition）是线性代数中一种重要的矩阵分解，是矩阵分析中正规矩阵酉对角化的推广。在信号处理、统计学等领域有重要应用
"""

'''1 加载测试数据集'''
def loadExData():
    return mat([[0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 5],
           [0, 0, 0, 3, 0, 4, 0, 0, 0, 0, 3],
           [0, 0, 0, 0, 4, 0, 0, 1, 0, 4, 0],
           [3, 3, 4, 0, 0, 0, 0, 2, 2, 0, 0],
           [5, 4, 5, 0, 0, 0, 0, 5, 5, 0, 0],
           [0, 0, 0, 0, 5, 0, 1, 0, 0, 5, 0],
           [4, 3, 4, 0, 0, 0, 0, 5, 5, 0, 1],
           [0, 0, 0, 4, 0, 4, 0, 0, 0, 0, 4],
           [0, 0, 0, 2, 0, 2, 5, 0, 0, 1, 2],
           [0, 0, 0, 0, 5, 0, 0, 0, 0, 4, 0],
           [1, 0, 0, 0, 0, 0, 0, 1, 2, 0, 0]])

def loadExData2():
    return mat([[5,5,0,5],
                [5,0,3,4],
                [3,4,0,3],
                [0,0,5,3],
                [5,4,4,5],
                [5,4,5,5]])

def format_float4(f):
    return float('%.4f' %(f))
"""
计算奇异值
M=u*sigma*v
任意的矩阵 M 是可以分解成三个矩阵
u 表示了原始域的标准正交基
v 表示经过 M 变换后的co-domain的标准正交基
sigma 表示了V 中的向量与u 中 相对应向量之间的关系,为对角矩阵
demo: M(6*4) = u(6*6) *sigma(6*4) *v(4*4)
"""
def calc_svd(dataMat,debug=False):
    u,sigma,vt=la.svd(dataMat)
    if debug:
        print u
        print '*'*10
        print sigma
        print '*'*10
        print vt
        print '*'*10
    return u,sigma,vt
"""
降维压缩
demo: M(6*4) 的奇异值矩阵sigma=6*4
降维到k=2
则sigma1=2*2,M则变为M1 = u1(6*2)*sigma1(2*2)*v1(4*2)
"""
def dimension_reduction(dataMat,k):
    u,sigma,vt=la.svd(dataMat)
    #set_trace()
    u1 = u[:,0:k]
    sigma1 = sigma[0:k]
    sigma1_diag = diag(sigma1)
    vt1 = vt[:,0:k]
    vt1_t = transpose(vt1)
    print u1
    print sigma1_diag
    print vt1_t
    return u1 * sigma1_diag * vt1_t
if __name__=='__main__':
    dataMat = loadExData2()
    debug = True
    u,sigma,vt = calc_svd(dataMat,debug)
    #print u
    #前两列
    #print u[:,0:2]

    #t = dimension_reduction(dataMat,2)
    #print t
