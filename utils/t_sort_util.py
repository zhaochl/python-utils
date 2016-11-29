#!/usr/bin/env python
# coding=utf-8

def test():
    print 'sort list'
    a=[4,5,3,6]
    b=sorted(a)
    print b
    a=[('b',2),('a',1),('c',0)]

    #a_tmp =a[i] like ('x',0),
    #a_tmp[0] = x,a_tmp[1] = 0

    b=sorted(a,key=lambda a_tmp:a_tmp[0])
    #[('a', 1), ('b', 2), ('c', 0)]
    print b
    
    b=sorted(a,key=lambda a_tmp:a_tmp[1])
    #[('c', 0), ('a', 1), ('b', 2)]
    print b

    b=sorted(a,key=lambda a_tmp:a_tmp[1],reverse=1)
    #[('b', 2), ('a', 1), ('c', 0)]
    print b

    #x,y 表示任意两个元素，x[0]表示第1个元素,x[1]，表示第2个元素
    b=sorted(a,cmp=lambda x,y:cmp(x[1],y[1]))
    #[('c', 0), ('a', 1), ('b', 2)]
    print b
    print 'sort dict'
    a={'b':2,'a':1,'c':0}
    b=sorted(a.iteritems(),cmp=lambda x,y:cmp(x[1],y[1]))
    print b
    b=sorted(a.iteritems(),cmp=lambda x,y:cmp(x[0],y[0]))
    print b

if __name__=='__main__':
    print '-test sort-'
    test()
