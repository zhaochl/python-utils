#!/usr/bin/env python
# coding=utf-8
from collections import *

def test_set():
    s=set('cheeseshop')
    print s,type(s)
    s=frozenset('cheeseshop')
    print s,type(s)
    
def test_dict():
    d = defaultdict(int)
    ll =[1,2,3]
    for l in ll:
        d[l]+=1
    print d
    for k,v in d.iteritems():
        print k,v
if __name__=='__main__':
    #test_set()
    test_dict()
