#!/usr/bin/python
# -*- coding: utf-8 -*-
from datetime import datetime
from datetime import *
import time
from math import *
def get_today_str():
    _n= datetime.datetime.now()
    return _n.strftime("%Y-%m-%d %H:%M:%S")

def get_today_str_last():
    _n= datetime.datetime.now()
    return _n.strftime("%Y-%m-%d %H-%M-%S")

def get_yesterday_str():
    _d=(datetime.datetime.now() - datetime.timedelta(days = 1))
    return _d.strftime("%Y-%m-%d %H:%M:%S")
def get_beforedays_str(before):
    _d=(datetime.datetime.now() - datetime.timedelta(days = int(before)))
    return _d.strftime("%Y-%m-%d %H:%M:%S")
def get_now_timestamp():
    return int(time.time())
def timestamp2str(timeStamp):
    timeArray = time.localtime(timeStamp)
    timestr = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return timestr
def str2timestamp(str1):
    _t = time.mktime(time.strptime(str1,'%Y-%m-%d %H:%M:%S'))
    return int(_t)

"""
like (base_str='20150920',1) = '20150919'
"""
def get_beforedays_str_based_str(base_str,before):
    _d = datetime.strptime(base_str,'%Y%m%d')
    _d2=_d - timedelta(days = int(before))
    return _d2.strftime("%Y%m%d")

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

"""
like n=datetime.now (n)='20160301'
"""
#把datetime转成字符串
def datetime_toString(dt):
    return dt.strftime("%Y-%m-%d")

"""
like 
str='20160301'
f()=datetime<>
"""
#把字符串转成datetime
def string_toDatetime(string):
    return datetime.strptime(string, "%Y-%m-%d")

#把字符串转成时间戳形式
def string_toTimestamp(strTime):
    return time.mktime(string_toDatetime(strTime).timetuple())

#把时间戳转成字符串形式
def timestamp_toString(stamp):
    return time.strftime("%Y-%m-%d", tiem.localtime(stamp))

#把datetime类型转外时间戳形式
def datetime_toTimestamp(dateTim):
    return time.mktime(dateTim.timetuple())

if __name__=='__main__':
    n = datetime.now()
    str = datetime_toString(n)
    print str 
    str='2015-01-01'
    d = string_toDatetime(str)
    print d
def test_old():
    pass
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
    '''
    #now = datetime.datetime.now()
    '''
    history = datetime.datetime(2016,1,15,13,14,15,16)
    historyStr = history.strftime('%Y-%m-%d %H:%M:%S')
    print history,historyStr
    _past_day = calc_past_day(historyStr)
    print _past_day
    '''
    
    #today = get_today_str()
    #print today
    #before1=get_beforedays_str(1)
    #print before1
