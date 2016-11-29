#!/usr/bin/env python
# coding=utf-8
"""
yield可以用来为一个函数返回值塞数据
"""
def add_list(l):
    for r in l:
        yield r+1

def yield_print():
    print 'hello'
    msg = yield 5
    print 'hello',msg

if __name__=='__main__':
    l = [0,1,2,3]
    l=add_list(l)
    print l
    for r in l:
        print r

    it = yield_print()
    it.next()
    it.send('zcl')
    it.next()
