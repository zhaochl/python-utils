#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
测试python 引用传递
"""
def add(d,k,v):
    if not d.has_key(k):
        d[k] =v
    return d

#{'a':{'a1':1,'b1':2}}
def create_hash_hash_isreplace(h,okey,ikey,val,isreplace=True):
    if not h.has_key(okey):
        _hashObj = {}
        _hashObj[ikey] = val
        h[okey] = _hashObj
    else:
        _hashObj  =  h[okey]
        if not _hashObj.has_key(ikey):
                _hashObj[ikey] = val
        else:
            if isreplace:
                _hashObj[ikey] = val
    return h
def search_hash_hash(h,okey,ikey=None):
    result = None
    if not ikey:
        if h.has_key(okey):
            _obj = h[okey]
            result = _obj
    else:
        if h.has_key(okey):
            _obj = h[okey]
            if _obj.has_key(ikey):
                result = _obj[ikey]
    return result

if __name__=='__main__':
    d={'a':1,'b':2}
    d2={}
    d2['d'] =d
    # {'d': {'a': 1, 'b': 2}}
    print d2
    print d2['d']
    for k,v in d.iteritems():
        print "k=%s,v=%s" %(k,v)
#------------------
    d= {}
    add(d,'a','1')
    add(d,'b',2)
    # {'a': '1', 'b': 2}
    print d
#-------------------
    h = {}
    h = create_hash_hash_isreplace(h,'a','a1',10)
    h = create_hash_hash_isreplace(h,'a','a2',20)
    h = create_hash_hash_isreplace(h,'a','a2',30,False) #replace
    h = create_hash_hash_isreplace(h,'b','b1',5)
    print h
    print 'demo main'
    r1 = search_hash_hash(h,'a')
    print r1
    r2=search_hash_hash(h,'a','a1')
    print r2

#=====
u = []
u.append('1')
u.append('1')
print u
print list(set(u))