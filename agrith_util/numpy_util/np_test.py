#!/usr/bin/env python
# coding=utf-8
import numpy as np

def gen_matrix(m,n):
    return np.zeros((m,n))

def list_to_np_array(l):
    return np.array(l)

def gen_matrix_n(x,y,z):
    return np.ones((x,y,z),dtype='int8')
def gen_matrix_from_file():
    return np.loadtxt('m.data', str, delimiter=':')
#创建对角阵
def get_diag(m):
    return np.diag(m)
def test_slice():
    #创建一维数组
    a = np.arange(36)
    #print a
    #转为二维数组
    b = a.reshape(6,6)
    print b
    """
    [[ 0  1  2  3  4  5 ]
     [ 6  7  8  9 10 11 ]
      [12 13 14 15 16 17]
       [18 19 20 21 22 23]
        [24 25 26 27 28 29]
         [30 31 32 33 34 35]]
    """
    #使用切片来读取第一行中的第二和第三个数，我们看下标【0,2:4】,其中逗号前的数字表示第0轴下标取值范围，逗号之后表示第1维下标取值范围，2:4就表示2-4之间
    c =b[0,2:4]
    # [2,3]
    print c
    d=b[0:2,0:2]
    #[[0,1],[6,7]]
    print d
    #第1行,[0 1 2 3 4 5]
    e=b[0,:]
    print e
    #第1列,[ 0  6 12 18 24 30 ],前两列 u[:,0:2]
    e=b[:,0]
    print e
    #设置步长（两个逗号后面的2表示步长为2）
    f=b[::2,::2]
    print f
if __name__=='__main__':
    t = gen_matrix(4,4)
    print t
    l=[1,2,3,4]
    print l
    m = np.mat(l)
    print m
    #一维数组转置，二维不需要
    m.shap = (5,1)
    print np.transpose(m)

    d = get_diag(l)
    print d
    t = gen_matrix_n(2,3,2)
    print t
    t=gen_matrix_from_file()
    print t
    test_slice()

