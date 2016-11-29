#!/usr/bin/env python
# coding=utf-8
import urllib2
import json
from urllib import urlencode
from urllib import quote
from urllib import unquote


def get_json_from_url(url):
    json_result = None
    try:
        req = urllib2.Request(url) 
        response = urllib2.urlopen(req) 
        the_page = response.read()
        #print the_page
        json_result = json.loads(the_page)
    except:
        print 'get data error,url:',url
    return json_result
def get_html_from_url(url,warn=True):
    _result = None
    try:
        req = urllib2.Request(url) 
        response = urllib2.urlopen(req) 
        the_page = response.read()
        _result =  the_page
    except:
        if warn:
            print 'get data error,url:',url
    return _result

def url_encode(para):
    para={'a':'1','b':'魔兽'}
    print urlencode(para)
    query = '京东 刘强东'
    print quote(query)
def url_decode(str):
    s='%C4%A7%CA%DE'
    t=unquote(s)
    t=t.decode('utf8')
    print t
if __name__=='__main__':
    """
    host = 'localhost'
    url = 'http://'+host+'/usercf?userid=3&projectid=17855&bejson=1' 
    r = get_json_from_url(url)
    print r
    url="http://localhost/search?query=a&bejson=1&crs=1&pagesize=200"
    r = get_json_from_url(url)
    print r
    url="http://www.jq22.com/demo/bootstrap-moban20150917/"
    t= get_html_from_url(url)
    print t
    """
    url_encode('')
    url_decode('')
