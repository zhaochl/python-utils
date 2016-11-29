#!/usr/bin/env python
# coding=utf-8
import json

def convert_jsonObj_to_string_recuse(jsonObj,results):
    #try:
        #t = eval(jsonStr)
    _results=''
    t=jsonObj
    print t
    if type(t)==str or type(t)==int:
        results+=str(t)+","
        _results+=str(t)+","
        print "results:",results
    else:
        if type(t)==dict:
            print 'dict'
            for k,v in t.iteritems():
                #print k,v
                _results += convert_jsonObj_to_string_recuse(v,results)       
        elif type(t)==list:
            print 'list:',t
            for _t in t:
                print t
                _results +=convert_jsonObj_to_string_recuse(_t,results)
    #except Exception,e :
    #    print "json_util - parse json_str error;e:",e
    return _results
if __name__=='__main__':
    print '--hello-json-'
    d ={'a':1,'b':2}
    #json_str= json.dumps(d)
    #print json_str
    #d2= json.loads(json_str)
    #print d2
    results = ''
    #d ={'a':1,'b':2}
    #d ={'a':1,'b':[{'c':3},{'d':3}]}
    d=[{'a':'a1'},{'b':[{'b1':'ss'},{'b2':'dd'}]}]
    t= convert_jsonObj_to_string_recuse(d,results)
    print 'results:'+results
    print t
