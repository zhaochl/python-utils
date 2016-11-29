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

def create_reverse_index_isrepeat(l,key,val,repeat):
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
'''求并集'''
def union_list(a,b):
    return list(set(a).union(set(b)))
'''求差集'''
def diff_list(a,b):
    return list(set(b).difference(set(a)))
'''求交集'''
def intersec_list(a,b):
    return list(set(a).intersection(set(b)))
'''
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
'''

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


if __name__=='__main__':
    print 'this is ds_util'
    a=[1,2,3]
    b=[3,4]
    c=union_list(a,b)
    print c
