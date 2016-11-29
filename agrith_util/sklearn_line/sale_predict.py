#!/usr/bin/env python
# coding=utf-8
from sklearn import linear_model #导入线性模型
import numpy as np
"""
通过历史数据计算：
TV Radio Newspaper
三者销量的相关性
"""
def read_file_line(file_name):
    file_doc = open(file_name ,'rb')
    lines = file_doc.readlines()
    file_doc.close()
    line_data=[]
    for line in lines:
        line = line.replace('\n','')
        line_data.append(line)
    return line_data

def calc():

    line_data = read_file_line('sale.data')
    #print line_data
    x_data =[]
    y_data =[]
    for i,l_data in enumerate(line_data):
        if i>0:
            l_data_list = l_data.split(' ')
            #print i,l_data_list
            x_data_one = []
            for j,d in enumerate(l_data_list):
                if j<len(l_data_list)-1:
                    x_data_one.append(float(d))
                else:
                    y_data.append(float(d))
            x_data.append(x_data_one)
    
    clf = linear_model.LinearRegression() 
    clf.fit(x_data,y_data)

    print clf.coef_  #系数矩阵
    #[ 1.09167788  0.05869232  0.37711143 ]
    # y =1.09167788*TV + 0.05869232*Radio + 0.37711143*Newspaper
    """
    说明的问题:
    对于给定了Radio和Newspaper的广告投入，如果在TV广告上每多投入1个单位，对应销量将增加0.0466个单位
    更明确一点，加入其它两个媒体投入固定，在TV广告上没增加1000美元（因为单位是1000美元），销量将增加46.6（因为单位是1000）
    """
    print clf.intercept_#截距
    x = np.array([100,100,100])

    y = x.dot(clf.coef_)
    print y
if __name__=='__main__':
    calc()
