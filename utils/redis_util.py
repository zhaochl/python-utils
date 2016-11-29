#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
create by zcl
at 2016
"""
import redis
import datetime
import json
#global rinst
default_server ='irnew'
def init_redis(tag=default_server):
    #rInst = redis.StrictRedis(host='localhost', port=6379, db=0)
    #rInst = redis.StrictRedis(host='localhost', port=6379, db=0)
    rInst =None
    if tag=='default_server':
        rInst = redis.StrictRedis(host='localhost', port=6379, db=0)
    elif tag =='irtest':
        rInst = redis.StrictRedis(host='localhost', port=6380, db=0)
    elif tag=='irnew':
        rInst = redis.StrictRedis(host='localhost', port=6381, db=0)
    return rInst

def get_keys_list(pattern,tag=default_server):

    _result=[]
    rInst = init_redis(tag)
    _result = rInst.keys(pattern)
    return _result
def del_keys(key,tag=default_server):
    _result = False
    rInst = init_redis(tag)
    return rInst.delete(key)
def get_string(key,tag=default_server):
    _result=None
    rInst = init_redis(tag)
    key = 'string:'+key
    if rInst.exists(key):
        _result = rInst.get(key)
    return _result
def set_string(key,value,tag=default_server):
    key = 'string:'+key
    rInst=init_redis(tag)
    rInst.set(key,value)

def get_json_to_dict(okey,tag=default_server):
    _result=None
    rInst = init_redis(tag)
    key = 'json:'+okey
    if rInst.exists(key):
        _result_tmp = rInst.get(key)
        if _result_tmp!=None:
            _result = json.loads(_result_tmp)
    return _result
def set_json_from_dict(okey,dict,tag=default_server):
    key = 'json:'+okey
    rInst=init_redis(tag)
    rInst.set(key,json.dumps(dict))

def get_hash_one(okey,ikey,tag=default_server):
    rInst=init_redis(tag)
    _result =0
    if rInst.exists(okey):
        _result = rInst.hget(okey,ikey)
    else:
        rInst.hset(okey,ikey,0)
        _result = 0
    if _result ==None:
        _result =0
    return _result
def get_hash_all(okey,tag=default_server):
    rInst=init_redis(tag)
    _result =None
    if rInst.exists(okey):
        _result = rInst.hgetall(okey)
    return _result
def del_hash_one(okey,ikey,tag=default_server):
    rInst=init_redis(tag)
    _result = False
    if rInst.exists(okey):
        _result = rInst.hdel(okey,ikey)
    return _result
def del_hash_all(okey,tag=default_server):
    rInst=init_redis()
    _hkey = 'hash:'+okey
    _result =False
    if rInst.exists(okey):
        _result = rInst.hgetall(okey)
        if _result!=None:
            _del_count=0
            for _k,_v in _result.iteritems():
                print _k,_v
                if rInst.hdel(okey,_k):
                    _del_count+=1
            if _del_count==len(_result):
                _result=True
    return _result
"""
return 
True - del success
False - del fail
"""
def set_hash_one(okey,ikey,val,tag=default_server):
    rInst=init_redis(tag)
    _hkey = 'hash:'+okey
    rInst.hset(okey,ikey,val)
def get_list(key,tag=default_server):
    _result = []
    rInst = init_redis(tag)
    if rInst.exists('list:'+key):
        _result = rInst.lrange('list:'+key,0,-1)
        #print _result
    return _result
def set_list(key,val,tag=default_server):
    rInst = init_redis(tag)
    #rInst.set('list:'+key,val)
    rInst.rpush('list:'+key,val)
def del_list_key(key,tag=default_server):
    rInst = init_redis(tag)
    if rInst.exists('list:'+key):
        rInst.delete('list:'+key)

def set_key_expire(key,ttl_second,tag=default_server):
    rInst = init_redis(tag)
    rInst.expire(key,ttl_second)

def set_key_expire_at(key,expire_time,tag=default_server):
    rInst = init_redis(tag)
    rInst.expireat(key,expire_time)

if __name__=='__main__':
    #key = "news_project_matchcount:1"
    #r= del_hash_all(key)
    #print r
    #r= del_hash_one(key,'15839')
    #print r
    """
    print 'this is redis_util main.'
    rInst = init_redis()
    set_string('s','s1')
    t=get_string('s')
    print t
    d={'a':1,'b':2}
    set_json_from_dict('dict',d)
    t=get_json_to_dict('dict')
    print t
    set_hash_one('h1','h',1)
    set_hash_one('h1','i',1)
    t = get_hash_one('h1','h')
    print t
    t = get_hash_all('h1')
    print t
    set_list('l1','a')
    set_list('l1','b')
    t=get_list('l1')
    print t
    """
    set_string('test','b')
    set_key_expire('string:test',60)
