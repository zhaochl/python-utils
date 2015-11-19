#!/usr/bin/python
# -*- coding: utf-8 -*-
#sudo apt-get install Python-bs4
from bs4 import BeautifulSoup
import re
import os

html_doc = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>

<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>

<p class="story">...</p>

"""
#soup = BeautifulSoup(html_doc)
pattern = re.compile(r'.*5.4.7.tar.gz')
base = 'http://archive.cloudera.com/cdh5/cdh/5/'
soup = BeautifulSoup(open('url.txt'))
for link in soup.find_all('a'):
        url = link.get('href')
	#print url
	match = pattern.match(url)
	if match:
		path =  base + match.group()
		print path
		#print 'downloading..file:'+path
		#download_info = os.popen('wget '+path+' -P download/')		
		#print download_info.read()






