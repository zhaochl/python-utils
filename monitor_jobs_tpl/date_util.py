#!/usr/bin/python
# -*- coding: utf-8 -*-
import datetime
import time
from math import *
def get_today_str():
    _n= datetime.datetime.now()
    return _n.strftime("%Y-%m-%d %H:%M:%S")
def get_yesterday_str():
    _d=(datetime.datetime.now() - datetime.timedelta(days = 1))
    return _d.strftime("%Y-%m-%d %H:%M:%S")
def get_paste_str(tag,num):
    #class datetime.timedelta([days[, seconds[, microseconds[, milliseconds[, minutes[, hours[, weeks]]]]]]])
    _result = None
    _d=None
    if tag=='day':
        _d=(datetime.datetime.now() - datetime.timedelta(days = num))
    elif tag=='min':
        _d=(datetime.datetime.now() - datetime.timedelta(minutes = num))
    elif tag=='hor':
        _d=(datetime.datetime.now() - datetime.timedelta(hours = num))
    else:
        print 'usage :get_paste_str(day/min/hor,n)'
    if _d !=None:
        _result = _d.strftime("%Y-%m-%d %H:%M:%S")
    return _result

def get_now_timestamp():
    return int(time.time())
def timestamp2str(timeStamp):
    timeArray = time.localtime(timeStamp)
    timestr = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return timestr
def str2timestamp(str1):
    _t = time.mktime(time.strptime(str1,'%Y-%m-%d %H:%M:%S'))
    return int(_t)

'''
date is string type 
calc score decay 
by zcl at 2016.1.7
'''
def calc_past_day(date):
    _result=0
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
        _result = _past_day
    return _result


if __name__=='__main__':
    '''
    print __file__
    print __name__
    print 'demo main.'
    today = get_today_str()
    print today
    yes = get_yesterday_str()
    print yes
    now_timestamp = get_now_timestamp()
    print now_timestamp

    timestr = timestamp2str(now_timestamp)
    print timestr
    a = "2011-09-28 10:00:00"
    print str2timestamp(a)
    
    #now = datetime.datetime.now()
    history = datetime.datetime(2016,1,15,13,14,15,16)
    historyStr = history.strftime('%Y-%m-%d %H:%M:%S')
    print history,historyStr
    _past_day = calc_past_day(historyStr)
    print _past_day
    '''

    today = get_today_str()
    print today
    t =  get_paste_str('hor',1)
    print t
