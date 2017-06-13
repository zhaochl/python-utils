#!/usr/bin/env python
# coding=utf-8

import urllib
import urllib2
import re
from bs4 import BeautifulSoup as BS
from pdb import *
def web():
    baseUrl = 'http://www.baidu.com/s'
    page = 1 #第几页
    word = '水滴筹'  #搜索关键词

    data = {'wd':word,'pn':str(page-1)+'0','tn':'baidurt','ie':'utf-8','bsst':'1'}
    data = urllib.urlencode(data)
    url = baseUrl+'?'+data

    try:
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)
    except urllib2.HttpError,e:
        print e.code
        exit(0)
    except urllib2.URLError,e:
        print e.reason
        exit(0)

    html = response.read()
    soup = BS(html)
    td = soup.find_all(class_='result')
    for t in td:
        title =  t.h3.a.get_text().replace('\n','').replace('','').strip()
        url = t.h3.a['href'].replace('\n','').replace(' ','').strip()
        if url.find('https://www.baidu.com/link')>=0:
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)
            content = response.read()
            #urls=re.findall(r"http://.*?\?fr=aladdin",content,re.I)
            urls = re.findall(r"\"http://.*?\"",content,re.I)+re.findall(r"\"https://.*?\"",content,re.I)
            if len(urls)>0:
                url = urls[0].strip("\"")
            else:
                set_trace()
        print title,url

def wap():
    baseUrl = 'http://m.baidu.com/s'
    page = 1 #第几页
    word = '水滴筹'  #搜索关键词

    data = {'wd':word,'pn':str(page-1)+'0','tn':'baidurt','ie':'utf-8','bsst':'1'}
    data = urllib.urlencode(data)
    url = baseUrl+'?'+data

    try:
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)
    except urllib2.HttpError,e:
        print e.code
        exit(0)
    except urllib2.URLError,e:
        print e.reason
        exit(0)

    html = response.read()
    soup = BS(html)
    #try:
    if 1:
        td = soup.find_all(class_='result')
        for index,t in enumerate(td):
            title=''
            url=''
            if t.h3:
                title= t.h3.get_text().replace('\n','').replace('','').strip()
                if t.h3.parent and t.h3.parent.has_key('href'):
                    url = t.h3.parent['href'].replace('\n','').replace(' ','').strip()
                    if url.find('https://www.baidu.com/link')>=0:
                        request = urllib2.Request(url)
                        response = urllib2.urlopen(request)
                        content = response.read()
                        #urls=re.findall(r"http://.*?\?fr=aladdin",content,re.I)
                        urls = re.findall(r"\"http://.*?\"",content,re.I)+re.findall(r"\"https://.*?\"",content,re.I)
                        if len(urls)>0:
                            url = urls[0].strip("\"")
                        else:
                            set_trace()
                print index,title,url
    #except Exception,e:
    #    print e
if __name__=='__main__':
    #wap()
    web()
