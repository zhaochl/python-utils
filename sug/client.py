#!/usr/bin/env python
# coding=utf-8
import sys
import httplib
import json

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'Usage: client inputs'
        exit
    try:
        httpClient = httplib.HTTPConnection('localhost', 5000, timeout=30)
        httpClient.request('GET', '/get_suggestion/'+sys.argv[1])
        response = httpClient.getresponse()
        sugs = json.loads(response.read())
        for sug in sugs:
            print sug['value']
    except Exception, e:
        print e
    finally:
        httpClient.close()
