#!/usr/bin/env python
# coding=utf-8
from Levenshtein import *
def levenshtein(first,second):
        if len(first) > len(second):
            first,second = second,first
        if len(first) == 0:
            return len(second)
        if len(second) == 0:
            return len(first)
        first_length = len(first) + 1
        second_length = len(second) + 1
        distance_matrix = [range(second_length) for x in range(first_length)] 
        #print distance_matrix
        for i in range(1,first_length):
            for j in range(1,second_length):
                deletion = distance_matrix[i-1][j] + 1
                insertion = distance_matrix[i][j-1] + 1
                substitution = distance_matrix[i-1][j-1]
                if first[i-1] != second[j-1]:
                    substitution += 1
                distance_matrix[i][j] = min(insertion,deletion,substitution)
        #print distance_matrix
        return distance_matrix[first_length-1][second_length-1]
"""
http://www.coli.uni-saarland.de/courses/LT1/2011/slides/Python-Levenshtein.html
"""
def  test():
    str1="abc"
    str2="abd"
    #计算 编辑距离 （也成 Levenshtein距离 ）。是描述由一个字串转化成另一个字串 最少 的操作次数，在其中的操作包括 插入 、 删除 、 替换 
    d=distance(str1,str2)
    print d
    #计算 汉明距离。 要求str1和str2必须长度一致。是描述两个等长字串之间 对应 位置上 不同 字符的个数
    d=hamming(str1,str2)
    print d
    #计算莱文斯坦比。计算公式  r = (sum - ldist) / sum, 其中sum是指str1 和 str2 字串的长度总和，ldist是 类编辑距离
    #ldist 类编辑距离不是2中所说的编辑距离，2中三种操作中每个操作+1，而在此处，删除、插入依然+1，但是替换+2
    #t=(6-2)/6
    t=ratio(str1,str2)
    print t
    steps = editops('spam', 'park')
    print steps
    #[('delete', 0, 0), ('insert', 3, 2), ('replace', 3, 3)]
    t= median(['SpSm', 'mpamm', 'Spam', 'Spa', 'Sua', 'hSam'])
    print t
if __name__=='__main__':
    #t=levenshtein('abc','abd')
    #print t 
    test()
