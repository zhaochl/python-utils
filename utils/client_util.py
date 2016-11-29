#!/usr/bin/env python
# coding=utf-8
import sys
import httplib
import json
import urllib
def get_url(url):
    result = None
    try:
        #httpClient = httplib.HTTPConnection('localhost', 1115, timeout=30)
        httpClient = httplib.HTTPConnection('localhost', 1115, timeout=30)
        httpClient.request('GET', urllib.quote(url))
        response = httpClient.getresponse()
        html = response.read()
        status = response.status
        reason = response.reason
        print html
        result = json.loads(html)
    except Exception, e:
        print e
    finally:
        httpClient.close()
    return result
def post_url():
    httpClient = None
    try:
        params = urllib.urlencode({'name': 'tom', 'age': 22})
        headers = {"Content-type": "application/x-www-form-urlencoded"
                        , "Accept": "text/plain"}
     
        httpClient = httplib.HTTPConnection("localhost", 80, timeout=30)
        httpClient.request("POST", "/test.php", params, headers)
     
        response = httpClient.getresponse()
        print response.status
        print response.reason
        print response.read()
        print response.getheaders() #获取头信息
    except Exception, e:
        print e
    finally:
        if httpClient:
            httpClient.close()
if __name__ == '__main__':
    #http://localhost:1115/rec_user?project_id=28294
    url ='/rec_user?project_id=28294'
    #url ='/list.html'
    t = get_url(url)
    print t
