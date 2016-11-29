#!/usr/bin/env python
# coding=utf-8
from redis_util import *
import redis

import json
import os
import logging
import logging.handlers

global __cache
__cache = {}
def set_cache(key,val):
    global __cache
    __cache[key] =val
def get_cache(key):
    global __cache
    __result = None
    if __cache. has_key(key):
        __result = __cache[key]
    return __result
def print_cache():
    global __cache
    print '---print cache info start--'
    for key,value in __cache.viewitems():
        print "key=%s, value=%s" % (key, value)
    print '---print cache info end--'
def C(key,val=None):
    global __cache
    __result = None
    # - get_cache
    if val==None:
        if __cache. has_key(key):
            __result = __cache[key]
    # - set_cache
    else:
        __cache[key] =val
    return __result
def CR(key,_fun):
    _cache_result = None
    if C(key)==None:
        _cache_result= _fun()
        C(key,_cache_result)
    else:
        _cache_result = C(key)
    return _cache_result

def S(key,type,val=None):
    key = 'cache:'+key
    _result = None
    rInst = redis.StrictRedis(host='localhost', port=6381, db=0)
    # - get_cache
    if val==None:
        #if __cache. has_key(key):
        #    __result = __cache[key]
        if rInst.exists(key):
            _result_tmp = rInst.get(key)
            if type=='string':
                _result = _result_tmp
            elif type=='json':
                if _result_tmp!=None:
                    _result = json.loads(_result_tmp)
    # - set_cache
    else:
        if type=='string':
            #__cache[key] =val
            rInst.set(key,val)
        elif type=='json':
            rInst.set(key,json.dumps(dict))
        _result=val
    return _result

def SR(key,_fun):
    _cache_result = None
    if S(key)==None:
        _cache_result= _fun()
        S(key,_cache_result)
    else:
        _cache_result = S(key)
    return _cache_result
def CF(key):
    _cache_result = None
    if C(key)==None:
        _cache_result= F(key)
        C(key,_cache_result)
    else:
        _cache_result = C(key)
    return _cache_result

"""
key = file_name
val = data,[] or {}
"""
def F(key,val=None):
    if key.find('/')==-1:
        key='cache/'+key
        logging.info('F() use default dir ./cache ')
    _result=None
    if val==None:
        _result = _get_json_from_dict_file(key)
        logging.info('get data from cache file ok')
    else:
        _set_json_to_dict_file(key,val)
        logging.info('set data to cache file ok')
        _result = 1
    return _result
def _write_file(file_name,str):
    pos = file_name.rfind('/')
    dir_path = file_name[:pos]
    if not os.path.exists(dir_path):
        #os.mkdir(dir_path)
        os.makedirs(dir_path)
        print 'mkdir '+dir_path+' ok'
    wordF= file( file_name,'w')
    wordF.write('%s' %(str))
    wordF.close()

def _read_file(file_name):
    fContent=""
    if not os.path.exists(file_name):
        return ""
    singleFile= file( file_name,'r')
    singleFile.seek(0)
    fContent = singleFile.read()
    singleFile.close()
    return fContent

def _set_json_to_dict_file(file_name,data):
    _write_file(file_name,json.dumps(data))
def _get_json_from_dict_file(file_name):
    d=None
    str = _read_file(file_name)
    if str!=None and str!="":
        d = json.loads(str)
    return d

if __name__=='__main__':
    '''
    set_cache('a',1)
    a = get_cache('a')
    print a

    set_cache('b',{'_b':1})
    set_cache('c',[1,2,3])
    t= get_cache('b')
    print t
    print_cache()
    
    a=C('a',1)
    print a
    b=C('a')
    print b
    '''
    #userList = C_user_list_all()
    #print len(userList)
    #print_cache()
    #a=set()
    #a.add('a1')
    #a.add('a2')
    #set_cache('a',a)
    #t=get_cache('a')
    #print t
    l=['a','b','c']
    F('test',l)
    t= F('test')
    print t
    d={'a':1,'b':2}
    F('test2',d)
    t=F('test2')
    print t
    t=F('cache_1')
    print t
