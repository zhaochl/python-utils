#!/usr/bin/python
# -*- coding: utf-8 -*-
from datetime import datetime
from datetime import *
import time
from math import *
import calendar
import re

"""
for sleep
"""
const_day_second = 86400
const_hour_second = 3600
const_week_second = 604800

def get_now_str():
    return time.strftime("%Y-%m-%d %H:%M:%S")

def get_today_str():
    _n= datetime.now()
    return _n.strftime("%Y-%m-%d %H:%M:%S")

def get_today_str_last():
    _n= datetime.datetime.now()
    return _n.strftime("%Y-%m-%d %H-%M-%S")

def get_today_str_start():
    _n= datetime.now()
    return _n.strftime("%Y-%m-%d ")+"00:00:00"
def get_today_str_end():
    _n= datetime.now()
    return _n.strftime("%Y-%m-%d ")+"23:59:59"


def get_yesterday_str():
    _d=(datetime.now() - timedelta(days = 1))
    return _d.strftime("%Y-%m-%d %H:%M:%S")
def get_beforedays_str(before):
    _d=(datetime.now() - timedelta(days = int(before)))
    return _d.strftime("%Y-%m-%d %H:%M:%S")

def get_beforedays_str_start(before):
    _d=(datetime.now() - timedelta(days = int(before)))
    return _d.strftime("%Y-%m-%d ")+"00:00:00"
def get_beforedays_str_end(before):
    _d=(datetime.now() - timedelta(days = int(before)))
    return _d.strftime("%Y-%m-%d ")+"23:59:59"

def get_beforeminute_str(before):
    _d=(datetime.now() - timedelta(minutes = int(before)))
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
    _today = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
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

'''
date is string type 
calc score decay 
by zcl at 2016.1.7
return int 
'''
def calc_past_week(date):
    _result=0
    _today = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
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
    #set_trace()
    # 1day = 86400s
    #print 'day_secs:',24*60*60
    _past_day = ceil(_past_sec/(86400*7))
    if _past_day>0:
        _result = _past_day
    return int(_result)


"""
like:
    to_time = '2016-03-28 23:59:59'
    t=get_future_days_str_based_str(to_time,3)
    t = '2016-03-31 23:59:59'
"""
def get_future_days_str_based_str(base_str,futuredays):
    format = '%Y-%m-%d %H:%M:%S'
    _d = datetime.strptime(base_str,format)
    _d2=_d + timedelta(days = int(futuredays))
    return _d2.strftime(format)



"""
like:
    from_time = '2016-03-27 00:00:00'
    to_time = '2016-03-28 23:59:59'
    t = calc_past_second_between(from_time,to_time)
    t=1
"""
def calc_past_second_between(date1,date2):
    _result=0
    
    _t1 = time.mktime(time.strptime(date1,'%Y-%m-%d %H:%M:%S'))
    _t2 = time.mktime(time.strptime(date2,'%Y-%m-%d %H:%M:%S'))
    
    _result = abs(int(_t2-_t1))
    return _result


"""
like:
    from_time = '2016-03-27 00:00:00'
    to_time = '2016-03-28 23:59:59'
    t = calc_past_second_between(from_time,to_time)
    t=1
"""
def calc_past_day_between(date1,date2):
    _result=0
    
    _t1 = time.mktime(time.strptime(date1,'%Y-%m-%d %H:%M:%S'))
    _t2 = time.mktime(time.strptime(date2,'%Y-%m-%d %H:%M:%S'))
    
    if int(_t2) > int(_t1):
        _result = int(_t2-_t1)
    else:
        print 'date1 must < date2'
        exit(1)
    _past_day = ceil(_result/const_day_second)
    _result = _past_day

    return _result



"""
like:
    from_time = '2016-03-27 00:00:00'
    to_time = '2016-03-28 23:59:59'
    t = calc_time_gap(from_time,to_time)
    t=1
"""
def calc_time_gap(date1,date2):
    _result=0
    
    _t1 = time.mktime(time.strptime(date1,'%Y-%m-%d %H:%M:%S'))
    _t2 = time.mktime(time.strptime(date2,'%Y-%m-%d %H:%M:%S'))
    _past_sec = 0
    if int(_t2) > int(_t1):
        _past_sec = int(_t2-_t1)
        #print '--',_past_sec
    else:
        print 'date1 must < date2'
        exit(1)
    # 1day = 86400s
    #print 'day_secs:',24*60*60
    _past_day = ceil(_past_sec/86400)
    #print 'pp',_past_day,_past_day>0.0,int(_past_day)>0
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


"""
return 201606
"""
def get_tomonth_str():
    _n= datetime.now()
    return _n.strftime("%Y%m")
"""
return if day = 01 True,else False
"""
def is_month_first_day():
    _result = False
    _n= datetime.now()
    _day = _n.strftime("%d")
    if _day=='01':
        _result = True
    else:
        _result = False

    return _result


def get_tomonth_days_count():
    now_year = time.localtime().tm_year
    now_month = time.localtime().tm_mon
    now_day = time.localtime().tm_mday
    month_range = calendar.monthrange(2016,7)
    return month_range[2]

def fix_month_str(m):
    m_str = str(m)
    if m<10:
        m_str = '0'+m_str
    return m_str
"""
split before days to server month 
return arrays before days (201609,20),(201508,30)
"""
def get_before_months(recent_day):
    #now_ymd = time.strftime("%Y-%m-%d")
    #now_ymd_arr = now_ymd.split('-')
    #now_year  = now_ymd_arr[0]
    #now_month = now_ymd_arr[1]
    #now_day = now_ymd_arr[2]
    now_datetime = datetime.now()
    
    #print now_datetime
    now_year = now_datetime.year
    now_month = now_datetime.month
    now_day = now_datetime.day
    #set_trace()
    now_year_month  = str(now_year) + fix_month_str(now_month)
    before_months = []
    
    now_month_range_tuple = calendar.monthrange(now_year,now_month)
    now_month_days_count = now_month_range_tuple[1]
    
    left = recent_day
    if left>now_day:
        left = left-now_day
        before_months.append([now_year_month,now_day])
    else:
        before_months.append([now_year_month,recent_day])
        return before_months


    before_month = now_month
    before_year = now_year
    while left>0:
        if before_month==1:
            before_month = 12
            before_year = before_year-1
        else:
            before_month = before_month-1
            before_year = before_year
        month_range_tuple = calendar.monthrange(before_year,before_month)
        month_days_count = month_range_tuple[1]
        before_year_month = str(before_year) + fix_month_str(before_month)
        
        left_new = left - month_days_count
        if left_new>0:
            before_months.append([before_year_month,month_days_count])
            left = left_new
        else:
            before_months.append([before_year_month,left])
            break
    return before_months
"""
return 201606
"""
def get_tomonth_str():
    _n= datetime.now()
    return _n.strftime("%Y%m")

"""
return 201606
"""
def get_now_table(table_prefix):
    _n= datetime.now()
    month = _n.strftime("%Y%m")
    return table_prefix+'_'+month
def test():
    #now year,month,day,hour,min
    print time.localtime()
    print time.localtime().tm_year
    month_range = calendar.monthrange(2016,7)
    print month_range
    table_prefix ='log'
    print get_now_table(table_prefix)


# 将计时器"时:分:秒"字符串转换为秒数间隔
def time2itv(sTime):

    p="^([0-9]+):([0-5][0-9]):([0-5][0-9])$"
    cp=re.compile(p)
    try:
        mTime=cp.match(sTime)
    except TypeError:
        return "[InModuleError]:time2itv(sTime) invalid argument type"

    if mTime:
        t=map(int,mTime.group(1,2,3))
        return 3600*t[0]+60*t[1]+t[2]
    else:
        return "[InModuleError]:time2itv(sTime) invalid argument value"


# 将秒数间隔转换为计时器"时:分:秒"字符串
def itv2time(iItv):

    if type(iItv)==type(1):
        h=iItv/3600
        sUp_h=iItv-3600*h
        m=sUp_h/60
        sUp_m=sUp_h-60*m
        s=sUp_m
        return ":".join(map(str,(h,m,s)))
    else:
        return "[InModuleError]:itv2time(iItv) invalid argument type"


if __name__=='__main__':
    #test()
    sTime="1223:34:15"
    print time2itv(sTime)
    print itv2time("451223")
    print itv2time("0.00225694444444")
def test2():
    n = datetime.now()
    str = datetime_toString(n)
    #print str 
    str='2015-01-01'
    d = string_toDatetime(str)
    #print d
    
    from_time = '2016-03-27 00:00:00'
    to_time = '2016-03-28 23:59:59'
    t = calc_past_second_between(from_time,to_time)
    print t

    #t= str2timestamp(to_time)
    #print t
    #t = calc_time_gap(from_time,to_time)
    #t=get_future_days_str_based_str(to_time,3)
    #print t
    #t=get_today_str()
    #print t
    #t=get_beforeminute_str(5)
    #print t
    t=calc_past_day(from_time)
    print t
    t=calc_past_week(from_time)
    print t
    t = get_now_str()
    print t
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
