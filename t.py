#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
s='zookeeper-3.4.5-cdh5.4.7-src.tar.gz'
s1='zookeeper-3.1.5-cdh5.1.7-src.tar.gz'

pattern = re.compile(r'.*5.4.7-.*.tar.gz')
match = pattern.match(s)
if match:
	print 'match'
	print match.group()

match = pattern.match(s1)
if match:
	print 'match'
	print match.group()
else:
	print 'not match'
