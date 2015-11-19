#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib2 

#from urllib import urlencode
req = urllib2.Request('http://www.pythontab.com') 
response = urllib2.urlopen(req) 
the_page = response.read()
print the_page

#---failed
#url='http://www.pythontab.com'
#data={"name":"hank", "passwd":"hjz"}
#header={"User-Agent": "Mozilla-Firefox5.0"}
#response=urllib2.urlopen(url, urllib.urlencode(data), header)
#print response
