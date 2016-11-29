#!/usr/bin/env python
# coding=utf-8

# -*- coding: utf-8 -*-
import MySQLdb
import urllib
import urllib2
import cookielib
import requests
from urllib import urlencode
# cookie set
# 用来保持会话
cj = cookielib.LWPCookieJar()
cookie_support = urllib2.HTTPCookieProcessor(cj)
opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
urllib2.install_opener(opener)

# default header
HEADER = {
    'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0',
    'Referer' : '*'
}

# operate method
def geturlopen(hosturl, postdata = {}, headers = HEADER):
    # encode postdata
    enpostdata = urllib.urlencode(postdata)
    # request url
    urlrequest = urllib2.Request(hosturl, enpostdata, headers)
    # open url
    urlresponse = urllib2.urlopen(urlrequest)
    # return url
    return urlresponse


def db_query(sql):
    conn = None
    cursor=None
    try:
        conn = MySQLdb.connect(host="localhost", port=3306,user="root", passwd="bd7c362280",db="yiyuan",charset="utf8",unix_socket="/tmp/mysql.sock")
        cursor = conn.cursor()
        cursor.execute("set NAMES utf8 ")
        cursor.execute(sql)
        results = cursor.fetchall()
        return results
    except MySQLdb.Error, e:
        print "error! --%d:  %s" % ( e.args[0], e.args[1]   )
        return None
    finally:
        if(cursor!=None):
            cursor.close()
        if(conn!= None):
            conn.close()


def load_activities():
    sql="""
    select id,total_need,already from activity where status=1;
    """
    result = db_query(sql)
    print result
    if result!=None and len(result)>1:
        for r in result:
            id = r[0]
            total_need = r[1]
            already = r[2]
            if float(already) >= float(total_need) * 0.8:
                print 'aid >80%',id,'robot start'


def login_post(aid,num):
    url="http://eduobao.ejzhi.com/index.php"
    #data = {"sessionToken":"ogyn4qq2how02pfn8dxu55bng"}

    url_login="http://eduobao.ejzhi.com/index.php?sessionToken=ogyn4qq2how02pfn8dxu55bng"


    #urlread = geturlopen(url,data)
    #html = urlread.read().decode('utf-8')
    #print html
    s = requests.Session()
    r=s.get(url_login)
    #r = s.get(url,auth=("sessionToken","ogyn4qq2how02pfn8dxu55bng"))
    #r = s.post(url,data)
    #r = requests.get(url,data)
    encoding = r.encoding
    html = r.text
    #print html

    url2="http://eduobao.ejzhi.com/index.php/index/t1"
    #r = s.get(url2)
    #html = r.text
    #print html
    #param = {"s22":"A]9|sw-d2o1$6qSyej&nJkHRx[vCPbOD\GEM*(L%X+Ni8ZfBp7T)5rIhgQtVc3^W4_uKmY0zFUal","s2":"gk3M%2&$IU\DtmyCuWJV[ez6FXqoY]4GQ^)|PANO9LvSn5lwrZs(p*_bjc71KRdxf+-8iETBHa0h","aid":1,"num":10}
    param = {"s1":"abc","s2":"123","aid":1,"num":10}
    param_str=""
    for k,v in param.iteritems():
        param_str+=str(k)+"="+str(v)+"&"
    #url_order=url2+"?"+urlencode(param)
    url_order=url2+"?"+param_str
    print url_order
    r = s.get(url_order)
    html = r.text
    print html

if __name__=='__main__':
    #print 'hello'
    load_activities()
    #login_post()
