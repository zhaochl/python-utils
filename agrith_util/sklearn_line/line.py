#!/usr/bin/env python
# coding=utf-8

#y=2x+1 (1,3)(2,5)(0,1)

from sklearn import linear_model #导入线性模型
import numpy as np

"""
y=0.5*x1+0.5*x2
[0,0,0]
[1,1,1]
[2,2,2]
X=[[0,0],[1,1],[2,2]]
y=[0,1,2]
"""
def calc_two():
    clf = linear_model.LinearRegression() #使用线性回归
    clf.fit ([[0, 0], [1, 1], [2, 2]], [0, 1, 2]) #对输入和输出进行一次fit，训练出一个模型
    #LinearRegression(copy_X=True, fit_intercept=True, n_jobs=1, normalize=False)
    print clf.coef_  #系数矩阵
    print clf.intercept_#截距
    #array([ 0.5,  0.5])
    #测试
    x = np.array([3,3])
    #y=0.5*3+0.5*3=3
    y = x.dot(clf.coef_)
    print y

if __name__=='__main__':
    calc_two()
