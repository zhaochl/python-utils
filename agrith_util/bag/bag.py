#!/usr/bin/env python
# coding=utf-8
from pdb import *

#n=5是物品的数量
#c=10是书包能承受的重量
#w=[2,2,6,5,4]是每个物品的重量
#v=[6,3,5,4,6]是每个物品的价值

def bag(n,c,w,v):
    res=[[-1 for j in range(c+1)] for i in range(n+1)]
    print res   
    for j in range(c+1):
        res[0][j]=0
    print res
    for i in range(1,n+1):
        for j in range(1,c+1):
            res[i][j]=res[i-1][j]
            if j>=w[i-1] and res[i][j]<res[i-1][j-w[i-1]]+v[i-1]:
                res[i][j]=res[i-1][j-w[i-1]]+v[i-1]
    return res

def show(n,c,w,res):
    print '最大价值为:',res[n][c]
    x=[False for i in range(n)]
    j=c
    for i in range(1,n+1):
        if res[i][j]>res[i-1][j]:
            x[i-1]=True
            j-=w[i-1]
    print('选择的物品为:')
    for i in range(n):
        if x[i]:
            print '第',i,'个,',x[i]
    print('')

if __name__=='__main__':
    n=5
    c=10
    w=[2,2,6,5,4]
    v=[6,3,5,4,6]
    res=bag(n,c,w,v)
    show(n,c,w,res)
    
