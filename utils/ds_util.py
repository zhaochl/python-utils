#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
create_reverse_index
reverse_index = [{'key1':[1,2,3]},{'key2':[1,3]}]
'''
def create_reverse_index(l,key,val):
    #print 'key:'+key

    if len(l)==0:
        l.append({key: [val]})
        return l

    for _i,_e in enumerate(l):
        #print _e
        #for k,v in _e.viewitems():
        #    print "k=%s, v=%s" % (k, v)
        if _e.has_key(key):
            #print 'True'
            _e[key].append(val)
            break
        else:
            if _i==(len(l)-1):
                #print 'false'
                l.append({key: [val]})
                break
    #print_list(l)
    return l
'''
repeat = True ,can be duplicate,[1,1,2]
repeat = Fase,can not be duplicate [1,2]
default ,not be duplicate
'''
def create_reverse_index_isrepeat(l,key,val,repeat =False):
    if len(l)==0:
         l.append({key: [val]})
         return l
    for _i,_e in enumerate(l):
        '''
        for key,value in _e.viewitems():
            print "key=%s, value=%s" % (key, value)
        '''
        if _e.has_key(key):
            #print 'True'
            if repeat == False:
                #print  _e[key]
                if val not in _e[key]:
                    _e[key].append(val)
                    #print 'not in'
            else:
                _e[key].append(val)

            break
        else:
            if _i==(len(l)-1):
                #print 'false'
                l.append({key: [val]})
                break
    return l
'''
author:chunliang
create date:2015-12-09
description: find the reverse index list for a key
    reverse_index = [{'key1':[1,2,3]},{'key2':[1,3]}]
    search('key1',reverse_index)=[1,2,3]
return: []
'''
def search_reverse_index(key,l):
    result=[]
    for r in l:
        if r.has_key(key):
            result = r[key]
            break
    return result
        #for k,v in r.viewitems():
        #    print "key=%s,value=%s"% (k,v)
"""
delete from rindex by key
like l=[{'a':[1,2,4],{'b':[3,4]}]
del_reverse_index_by_key('a',l)
return l=[{'b':[3,4]}]
"""
def del_reverse_index_by_key(key,l):
    result_l = l
    for i,r in enumerate(l):
        if r.has_key(key):
            result_l.remove(r)
            print 'del:',r
            break
    return result_l

'''求并集'''
def union_list(a,b):
    return list(set(a).union(set(b)))
'''求差集'''
def diff_list(a,b):
    return list(set(b).difference(set(a)))
'''求交集'''
def intersec_list(a,b):
    return list(set(a).intersection(set(b)))

def print_list(l):
    print '---print list info start--'
    for _l in l:
        print _l
    print '--print list info end---'
def print_dict(d):
    print '---print dict info start--'
    for key,value in d.viewitems():
        print "key=%s, value=%s" % (key, value)
    print '---print dict info end--'
def print_reverse_index(l):
    print '---print reverse info start--'
    for _e in l:
        #print _l
        for k,v in _e.viewitems():
            print "k=%s, v=%s" % (k, v)
    print '--print reverse index info end---'

#json array util
# {'101': [{'123': 0.9},{'121': 0.1}],'102':[{'11':0.2}]}
def create_json_array(dict,outKey,inKey,inVal):
    if(dict.has_key(outKey)):
        outKeyList = []
        if dict[outKey] != None:
            outKeyList = dict[outKey]
            for obj in outKeyList:
                if(not obj.has_key(inKey)):
                    obj[inKey] = inVal
    else:
        dict[outKey] = []
        dict[outKey].append({inKey: inVal})
    return dict

def search_json_array(dict,outKey):
    if(dict.has_key(outKey)):
        return dict[outKey]
    else:
        return None

                                                                                              
#{'a':{'a1':1,'b1':2}} 
# create at 12.22
# author zcl
def create_hash_hash_isreplace(h,okey,ikey,val,isreplace=True):                               
    if not h.has_key(okey):                                                                   
        _hashObj = {} 
        if okey !=0:
            _hashObj[ikey] = val                                                                  
            h[okey] = _hashObj                                                                    
    else:                                                                                     
        _hashObj  =  h[okey]                                                                  
        if not _hashObj.has_key(ikey) and ikey != 0:                                                        
                _hashObj[ikey] = val                                                          
        else:                                                                                 
            if isreplace:                                                                     
                _hashObj[ikey] = val                                                          
            else:
                _hashObj[ikey] += val                                                          
    return h                                                                                  
'''
dict has key(key)
if has int(key) or str(key)
return true
add by zcl at 2016.1.19
'''
def dict_has_key(d,key):
    _result=False
    if d==None:
        return _result
    else:
        if d.has_key(key):
            _result = 0
        elif d.has_key(int(key)):
            _result = 1
        elif d.has_key(str(key)):
            _result = -1
    return _result
def search_hash_hash(h,okey,ikey=None):                                                       
    result = None                                                                             
    if h == None:
        return result
    if not ikey:                                                                              
        if h.has_key(okey):                                                                   
        #if dict_has_key(h,okey):                                                                   
            _obj = h[okey]                                                                    
            result = _obj                                                                     
    else:                                                                                     
        if h.has_key(okey):                                                                   
        #if dict_has_key(h,okey):                                                                   
            _obj = h[okey]                                                                    
            if _obj.has_key(ikey):                                                            
            #if dict_has_key(_obj,ikey):                                                            
                result = _obj[ikey]                                                           
    return result   

'''
create_inverse_index_hash
reverse_index = {'key1':[1,2,3],'key2':[1,3]}

create_reverse_index
reverse_index = [{'key1':[1,2,3]},{'key2':[1,3]}]
'''

def create_reverse_index_hash(h,key,val):
    if len(h)==0:
        h = {key:[val]}
    else:
        if h.has_key(key):
            h[key].append(val)
        else:
            h[key] = [val]
    return h
"""
按照倒排中的key对应的list值长度进行升序、倒序
"""
def order_reverse_index_by_key_len(rIndex,tag='asc'):
    rdict = {}
    _reverse=True
    if tag=='asc':
        _reverse = False
    else:
        _reverse = True
    _index=0
    for _index,o in enumerate(rIndex):
        for _topic_id,_pidList in o.iteritems():
            l =  len(_pidList)
            rdict[_index] = l

    rdict=sorted(rdict.items(), lambda x, y: cmp((x[1]), (y[1])), reverse=_reverse)
    #print rdict
    rindex_order=[]
    for _index,_len in rdict:
        rindex_order.append(rIndex[_index])
    rindex = rindex_order
    return rindex

if __name__=='__main__':
    print 'this is ds_util'
    a=[1,2,3]
    b=[3,4]
    c=union_list(a,b)
    print c

    rl = [{'key1':[1,2,3]},{'key2':[1,3]}]
    t= del_reverse_index_by_key('key1',rl)
    print t
    t= del_reverse_index_by_key('key2',rl)
    print t    
    h={}
    h=create_reverse_index_hash(h,'a',1)
    h=create_reverse_index_hash(h,'a',2)
    h=create_reverse_index_hash(h,'b',1)
    print h
    print '#----test order_reverse_index_by_key_len--'
    rl = [{'key1':[1]},{'key2':[1,3,2]},{'key3':[2,3]}]
    print rl
    t= order_reverse_index_by_key_len(rl,'asc')
    print t
