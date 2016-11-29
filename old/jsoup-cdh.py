#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib2 
from bs4 import BeautifulSoup

req = urllib2.Request('http://archive.cloudera.com/cdh5/cdh/5') 
#req = urllib2.Request('http://news.sohu.com/') 
response = urllib2.urlopen(req) 
the_page = response.read()
#print the_page

soup = BeautifulSoup(the_page)
for link in soup.find_all('a'):
	print link.get('href')
