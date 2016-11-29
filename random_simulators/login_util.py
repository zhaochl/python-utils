#!/usr/bin/env python
# coding=utf-8

import MySQLdb
import urllib
import urllib2
import cookielib
import requests
from random import *
from urllib import urlencode

def login_post(uname,uid,aid,num):
    url="http://eduobao.ejzhi.com/index.php"
    url_login="http://eduobao.ejzhi.com/index.php?sessionToken=ogyn4qq2how02pfn8dxu55bng"

    s = requests.Session()
    r=s.get(url_login)
    encoding = r.encoding
    html = r.text
    url2="http://eduobao.ejzhi.com/index.php/index/t1"
    param = {
"sOKxEu57kDvZhfBR3ITGFP14wi02NLl6rtUpodYMmb8eyXaScCVzQWjHqg9nAJ":"CDU16ELjtfhBzFR9580oKSIc3v2QlmHxa7gArpkZMXNwVbn4GsWJduyTePqiYO",
"MmOBSagpvxtDTJUGb945iqe6ozKHfdP2hFQjk1yVuwYACLn0ZNWc7lX3E8IsrR":"bXak3O46UjFIVBw0os9tHxKncqTp7rJlMh1dvD5g8mLiyzQNAuE2WeZPYGSCRf",
"c9Bk5Wv":aid,
"Gl5rbjY":num,
"eyiBM1P":uid,
"oQDFh6G":uname
}
    #param = {"s2":"abc","s2":"123","aid":aid,"num":num}
    param_str=""
    for k,v in param.iteritems():
        param_str+=str(k)+"="+str(v)+"&"
    #url_order=url2+"?"+urlencode(param)
    url_order=url2+"?"+param_str
    print url_order
    r = s.get(url_order)
    html = r.text
    print html
    s.close()
