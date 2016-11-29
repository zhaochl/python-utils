#!/usr/bin/env python
# coding=utf-8
from operator import itemgetter, attrgetter

from random import *

l = range(10)
print l
#shuffle() 方法将序列的所有元素随机排序
shuffle(l)
print l

if __name__ == '__main__':
    d={'k1':3,'k2':5,'k3':4}
    #对由字典排序 ，返回由tuple组成的List,不再是字典
    # dict中,按照 value进行降序
    t=sorted(d.items(), lambda x, y: cmp((x[1]), (y[1])), reverse=True)[0:2]
    print t
    
    #list - 按照元素长度排序
    l = [{1:5,3:4},{1:3,6:3},{1:1,2:4,5:6},{1:9}]
    def f(x):
        return len(x)
    l=sorted(l,key=f)
    print l

    #按照每个字典元素里面key为1的元素的值排序
    L = [{1:5,3:4},{1:3,6:3},{1:1,2:4,5:6},{1:9}]
    def f2(a,b):
        return a[1]-b[1]
    L.sort(cmp=f2)
    print L
    
    results_data = [
        {'query': 'a', 'rate_this_week': '1.2%', 'r': '1.1878%'},
        {'query': 'b', 'rate_this_week': '1.2512%', 'r': '0.6478%'}, 
        {'query': 'c', 'rate_this_week': '0.1612%', 'r': '0.6478%'}]
    def _sort_stat_hot_query(a,b):
        a1= a['rate_this_week']
        a2= b['rate_this_week']
        #print a1,a2
        a11 = a1.strip('%')
        a22 = a2.strip('%')
        #print a11,a22
        return int((float(a11)-float(a22))*10000)
    results_data.sort(cmp=_sort_stat_hot_query,reverse=True)
    print results_data
    
    #对于tuple中某一列排序
    #key
    students = [('john', 'A', 15), ('jane', 'B', 9), ('dave', 'C', 10)]
    t=sorted(students, key=lambda student : student[2])   # sort by age
    print t
    #cmp排序
    t=sorted(students, cmp=lambda x,y : cmp(x[2], y[2])) # sort by age 
    print t
    #operator-getattr
    t=sorted(students, key=itemgetter(2)) 
    print t
    #用 operator 函数进行多级排序
    t=sorted(students, key=itemgetter(1,2))  # sort by grade then by age 
    print t
    infoList = [[1,100],[3,300],[2,200]]
    t = sorted(infoList, lambda x, y: cmp((x[1]),(y[1])), reverse=False)
    print t
    infoList =[1,3,2]
    t=sorted(infoList)
    print t
    results_data = [{'query':'a','count':1.4},{'query':'b','count':2.1},{'query':'c','count':1.8}]
    results_data =sorted(results_data, lambda x, y: cmp((x['count']), (y['count'])), reverse=True)[0:200]
    print results_data

    #action_data = sorted(action_data, lambda x, y: cmp((x[5]), (y[5])), reverse=True)
