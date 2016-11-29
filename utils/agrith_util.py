#!/usr/bin/python
# -*- coding: utf-8 -*-
#dbg=False
dbg=True
from math import *
import datetime
import time
"""
计算两个dict 向量的余弦相似度
cosine(a,b) = a*b / |a|*|b| =x / y
demo:
d1 = {'A':1,'B':2}
d2 = {'B':2,'C':1}
sim = calcCosine(d1,d2) ##0.8
优化策略，可以将d1的模存在d1里面，减少每次的模计算
"""
def calcCosine(dict1,dict2):

    x=0.0
    y=0.0
    y1=0.0
    y2=0.0
    for k1,v1 in dict1.iteritems():
        y1 += pow(float(v1),2)
        #if dbg: print '--',k1,v1,y1
    for k2,v2 in dict2.iteritems():
        y2 += pow(float(v2),2)
    for k2,v2 in dict2.iteritems():
        #if dbg: print '==',k2,v2,y2
        
        # a1*b1+a2*b2.. 自动补全计算集合
        if dict1.has_key(k2):
            dk2_val = float(dict1[k2])
            #print x,v2,k2,dk2_val
            x+= float(v2)* dk2_val
            #x+= v2* float(dict1[k2])
    #if dbg: print '**',x,y1,y2
    y = sqrt(y1) * sqrt(y2)
    """
    #jsut for test
    if x!=0 and y1 !=0 and y2 !=0:
        print '----info---'
        print dict1
        print dict2
        print x,y1,y2,x/y
    """
    if y==0:
        return 0.0
    else:
        #if x/y !=0:
        #    print 'result:',x/y
        return  x/y



def calcCosine2(dict1,dict2):

    x=0.0
    y=0.0
    y1=0.0
    y2=0.0
    result=0.0

    for k1,v1 in dict1.iteritems():
        y1 += pow(float(v1),2)
        #if dbg: print '--',k1,v1,y1
    for k2,v2 in dict2.iteritems():
        y2 += pow(float(v2),2)
    for k2,v2 in dict2.iteritems():
        #if dbg: print '==',k2,v2,y2
        
        # a1*b1+a2*b2.. 自动补全计算集合
        if dict1.has_key(k2):
            dk2_val = float(dict1[k2])
            #print x,v2,k2,dk2_val
            x+= float(v2)* dk2_val
            #x+= v2* float(dict1[k2])
    #if dbg: print '**',x,y1,y2
    y = sqrt(y1) * sqrt(y2)
    """
    #jsut for test
    if x!=0 and y1 !=0 and y2 !=0:
        print '----info---'
        print dict1
        print dict2
        print x,y1,y2,x/y
    """
    if y>0:
        result = x/y

    return result 
'''
calcCosine_item
p1={u1:0.2,u2:0.3},keys=[u1,u2],lenk1=2
p2={u1:0.3,u3:0.4},keys=[u1,u3],lenk2=2
sim(p1,p2) = len(p1.keys & p2.keys) /sqrt(len(p1.keys) *len(p2.keys))
           =len([u1])/sqrt(2*2) = 1/2 = 0.5
'''
def calcCosine_item(dict1,dict2):
    _result = 0.0
    if dict1==None or dict2==None or len(dict1)==0 or len(dict2)==0:
        return _result
    _d1_klist = dict1.keys()
    _d1_klen = len(_d1_klist)

    _d2_klist = dict2.keys()
    _d2_klen = len(_d2_klist)

    #list(set(a).intersection(set(b)))
    #_inter_list = intersec_list(_d1_klist,_d2_klist)
    _inter_list = list(set(_d1_klist).intersection(set(_d2_klist)))
    _inter_len = len(_inter_list)
    if(_inter_len>0 and _d1_klen>0 and _d2_klen):
        #_result = _inter_len /sqrt(_d1_klen*_d2_klen)
        # -test onece-
        _result = _inter_len
    return _result
'''
计算一个值的半衰期
by zcl at 2016.1.7
'''
#m=M(1/2)^(t/T)
def half_life_decay(val,t,T):
    _result=0.0
    if T!=0:
        _result=val * pow(0.5,t/T)
    return _result
def sim_half_life_decay(sim,date):
    _T=3
    _result = sim
    
    _today = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #_t = datetime.datetime.now()
    #print 'now:',_today
    #_d = datetime.datetime.strptime(date,'%Y-%m-%d %H:%M:%S')
    #print 'date:',_d
    
    _t1 = time.mktime(time.strptime(_today,'%Y-%m-%d %H:%M:%S'))
    _t2 = time.mktime(time.strptime(date,'%Y-%m-%d %H:%M:%S'))
    _past_sec = 0
    if int(_t1) > int(_t2):
        _past_sec = int(_t1-_t2)
        #print _past_sec
    
    # 1day = 86400s
    #print 'day_secs:',24*60*60
    _past_day = ceil(_past_sec/86400)
    if _past_day>0:
        _result = half_life_decay(sim,_past_day,_T)
        #print 'sim - decay:',_result
    return _result
'''
date is string type 
calc score decay 
by zcl at 2016.1.7
'''
def score_half_life_decay(score,date):
    _T=3
    _result = score
    
    _today = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #_t = datetime.datetime.now()
    #print 'now:',_today
    #_d = datetime.datetime.strptime(date,'%Y-%m-%d %H:%M:%S')
    #print 'date:',_d
    
    _t1 = time.mktime(time.strptime(_today,'%Y-%m-%d %H:%M:%S'))
    _t2 = time.mktime(time.strptime(date,'%Y-%m-%d %H:%M:%S'))
    _past_sec = 0
    if int(_t1) > int(_t2):
        _past_sec = int(_t1-_t2)
        #print _past_sec
    
    # 1day = 86400s
    #print 'day_secs:',24*60*60
    _past_day = ceil(_past_sec/86400)
    
    #print _past_day
    if _past_day>0:
        _result = half_life_decay(score,_past_day,_T)
        #print 'sim - decay:',_result
    return _result
if __name__=='__main__':
    #----test for calcCosine --
    """
    print __file__
    print __name__
    d1 = {'A':1,'B':2}
    d2 = {'B':2,'C':1}
    sim = calcCosine(d1,d2)
    print 'result is:',sim
    """

    #----test for half_life_decay--
    """
    decay = half_life_decay(1,8,8)
    print decay
    decay = half_life_decay(1,6,2)
    print decay
    """
    #----test for sim_half_life_decay--
    '''
    sim = 0.1
    date='2016-1-01 12:01:01'
    _today = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    _t1 = time.mktime(time.strptime(_today,'%Y-%m-%d %H:%M:%S'))
    _t2 = time.mktime(time.strptime(date,'%Y-%m-%d %H:%M:%S'))
    _past_sec = 0
    if int(_t1) > int(_t2):
        _past_sec = int(_t1-_t2)
    _past_day = ceil(_past_sec/86400)
    print '--delta:--',_past_day 
    r = sim_half_life_decay(sim, date)
    print r
    score = 10
    date='2016-1-01 12:01:01'
    r = score_half_life_decay(score, date)
    print r
    '''


    #_today = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #print _today
    '''
    d1 = {'10014':float(2.3283064365386963e-09),'8371': 1.8479780433329295e-09,'9957':1.1641532182693481e-09,'9594':1.1641532182693481e-09}
    d2 = {'10014':float(4.6935716640013165e-08)}
    sim = calcCosine2(d1,d2)
    print 'result is:',sim
    '''
