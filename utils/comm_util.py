#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
Debug=0
def dp(debug,content):
    if debug==1:
        print str(content)
def print_list(l):
    if len(l)>0:
        print '---print list info start--'
        for _l in l:
            print _l
        print '--print list info end---'
def print_dict(d):
    if len(d)>0:
        print '---print dict info start--'
        for key,value in d.viewitems():
            print "key=%s, value=%s" % (key, value)
        print '---print dict info end--'
def print_reverse_index(l):
    if len(l)>0:
        print '---print reverse info start--'
        for _e in l:
            #print _l
            for k,v in _e.viewitems():
                print "k=%s, v=%s" % (k, v)
        print '--print reverse index info end---'
def die():
    exit(1)
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
            _result = True
        elif d.has_key(int(key)):
            _result = True
        elif d.has_key(str(key)):
            _result = True
    return _result

def b():
    pass
class c:
    pass
 
def type_test():
    a = 10
    #True
    print isinstance(a,(int,str))
    #False
    print isinstance(a,(float,str))
    #False
    print isinstance(b,(str,int))
    
    obj = c()
    #True
    print isinstance(obj,(c,int))
"""
input 0.112123
return 11.21%
"""
def format_float_to_percent(f):
    return ('%.2f' %(f*100))+'%'

def format_float_to_percent4(f):
    return ('%.4f' %(f*100))+'%'

def format_percent_to_float(p):
    t = p.strip('%')
    return float(t)
"""
input 0.112123
return 0.11
"""
def format_float(f):
    return float('%.2f' %(f))

def format_float4(f):
    return float('%.4f' %(f))
def convert_dict_string():
    _str=''
    d={'a':1,'b':2}
    for k,v in d.viewitems():
        _str+=k+':'+str(v)+','
    return _str.strip(',')
def test():
    print 'demo main.'
    dp(1,'--dp test--')
    t=format_float_to_percent(-0.10)
    print t
    t=format_float(0.1111)
    print t   
    dp(2,'--nothing to show--')
    t=convert_dict_string()
    print t
def run(debug):
    if debug:
        print 'debuging'
    else:
        print 'online runing'
if __name__=='__main__':
    debug = True
    if len(sys.argv)>1:
        debug_str = sys.argv[1]
        if debug_str=='True':
            debug = True
        else:
            debug = False
    print 'debug:',debug
    run(debug)
