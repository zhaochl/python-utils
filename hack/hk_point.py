#!/usr/bin/env python
# coding=utf-8
from http_util import *
from datetime import datetime
from datetime import *
import time
def get_beforedays_str(before):
    _d=(datetime.now() - datetime.timedelta(days = int(before)))
    return _d.strftime("%Y%m%d")
def point(datestr):
    #url ="http://www.jq22.com/demo/bootstrap-moban20150920/"
    url ="http://www.jq22.com/demo/bootstrap-moban"+datestr

def get_beforedays_str_based_str(base_str,before):
    _d = datetime.strptime(base_str,'%Y%m%d')
    _d2=_d - timedelta(days = int(before))
    return _d2.strftime("%Y%m%d")


def hack_main():
    count =365*2
    timegap = range(count)
    #str1='20150917'
    str1='20160323'
    #print timegap
    for i,v in enumerate(timegap):
        #print i,v
        #_d = get_beforedays_str(v)
        datestr = get_beforedays_str_based_str(str1,v)

        url ="http://www.jq22.com/demo/bootstrap-moban"+datestr+"/"
        html = get_html_from_url(url,False)
        if html!=None:
            print url
if __name__=='__main__':
    hack_main()
    #str1='20150920'
    #d = get_beforedays_str_based_str(str1,1)
    #print d
