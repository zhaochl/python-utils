#!/usr/bin/python
# -*- coding: utf-8 -*-
# encoding: UTF-8
import re
# 将正则表达式编译成Pattern对象
pattern = re.compile(r'hello')
# 使用Pattern匹配文本，获得匹配结果，无法匹配时将返回None
match = pattern.match('hello world!')
if match:
	#使用Match获得分组信息
    print match.group()
### 输出 ###
# hello

m = re.match(r'hello', 'helloss')
print m.group()

p=re.compile(r'\d+')
#d = re.match(r'\d', 'hello world 123')
#print 'd:'+d
#if d:
#	print d.group()
res=p.findall('hello world123')
print res
print res[0]
p = re.compile(r'\d+')
print p.findall('one1two2three3four4')
### output ###
# ['1', '2', '3', '4']

p = re.compile(r'\d+')
print p.split('one1two2three3four4')
### output ###
# ['one', 'two', 'three', 'four', '']

p = re.compile(r'\d+')
for m in p.finditer('one1two2three3four4'):
	print m.group()
### output ###
# 1 2 3 4

#----------------match---
m = re.match(r'(\w+) (\w+)(?P<sign>.*)', 'hello world!')
 
print "m.string:", m.string
print "m.re:", m.re
print "m.pos:", m.pos
print "m.endpos:", m.endpos
print "m.lastindex:", m.lastindex
print "m.lastgroup:", m.lastgroup
 
print "m.group(1,2):", m.group(1, 2)
print "m.groups():", m.groups()
print "m.groupdict():", m.groupdict()
print "m.start(2):", m.start(2)
print "m.end(2):", m.end(2)
print "m.span(2):", m.span(2)
print r"m.expand(r'\2 \1\3'):", m.expand(r'\2 \1\3')
 
### output ###
# m.string: hello world!
# m.re: <_sre.SRE_Pattern object at 0x016E1A38>
# m.pos: 0
# m.endpos: 12
# m.lastindex: 3
# m.lastgroup: sign
# m.group(1,2): ('hello', 'world')
# m.groups(): ('hello', 'world', '!')
# m.groupdict(): {'sign': '!'}
# m.start(2): 6
# m.end(2): 11
# m.span(2): (6, 11)
# m.expand(r'\2 \1\3'): world hello!

#-----------------pattern--------
p = re.compile(r'(\w+) (\w+)(?P<sign>.*)', re.DOTALL)
 
print "p.pattern:", p.pattern
print "p.flags:", p.flags
print "p.groups:", p.groups
print "p.groupindex:", p.groupindex
 
### output ###
# p.pattern: (\w+) (\w+)(?P<sign>.*)
# p.flags: 16
# p.groups: 3
# p.groupindex: {'sign': 3}
