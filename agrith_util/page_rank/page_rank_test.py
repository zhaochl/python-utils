#!/usr/bin/env python
# coding=utf-8
#-*- coding:utf-8 -*-
import random

N = 8           #八个网页
d = 0.85        #阻尼因子为0.85
delt = 0.00001  #迭代控制变量
#两个矩阵相乘
def matrix_multi(A,B):
    result = [[0]*len(B[0]) for i in range(len(A))]
    for i in range(len(A)):
        for j in range(len(B[0])):
            for k in range(len(B)):
                result[i][j] += A[i][k]*B[k][j] 
    return result

#矩阵A的每个元素都乘以n
def matrix_multiN(n,A):
    result = [[1]*len(A[0]) for i in range(len(A))]
    for i in range(len(A)):
        for j in range(len(A[0])):
            result[i][j] = n*A[i][j]
    return result

#两个矩阵相加
def matrix_add(A,B):
    if len(A[0])!=len(B[0]) and len(A)!=len(B):
        return
    result = [[0]*len(A[0]) for i in range(len(A))] 
    for i in range(len(A)):
        for j in range(len(A[0])):
            result[i][j] = A[i][j]+B[i][j]
    return result 

def pageRank(A):
    e = []
    for i in range(N):
        e.append(1) 
    norm = 100
    New_P = []
    for i in range(N):
        New_P.append([random.random()]) 
    r = [ [(1-d)*i*1/N] for i in e]
    while norm > delt:
        P = New_P
        New_P = matrix_add(r,matrix_multiN(d,matrix_multi(A,P))) #P=(1-d)*e/n+d*M'P PageRank算法的核心
        norm = 0
        #求解矩阵一阶范数
        for i in range(N):
            norm += abs(New_P[i][0]-P[i][0])
    print New_P

#根据邻接矩阵求转移概率矩阵并转向
def tran_and_convert(A):
    result = [[0]*len(A[0]) for i in range(len(A))]
    result_convert = [[0]*len(A[0]) for i in range(len(A))]
    for i in range(len(A)):
        for j in range(len(A[0])):
            result[i][j] = A[i][j]*1.0/sum(A[i])
    for i in range(len(result)):
        for j in range(len(result[0])):
            result_convert[i][j]=result[j][i]
    return result_convert


def main():
    A = [[0,1,1,0,0,1,0,0],\
    [0,0,0,1,1,0,0,0],\
    [0,0,0,1,0,1,0,0],\
    [0,0,0,0,0,1,0,0],\
    [1,0,0,1,0,0,1,1],\
    [0,0,0,1,0,0,0,0],\
    [0,0,1,0,0,0,0,0],\
    [0,0,0,1,0,0,1,0]]
    M = tran_and_convert(A)
    pageRank(M)

if __name__ == '__main__':
    main()

