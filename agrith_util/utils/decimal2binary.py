#!/usr/bin/env python
#coding: utf8


#http://my.oschina.net/goal/blog/200347

#bin(number) -> string
#十进制转换为二进制
a=50
print bin(50)#0b110010
print bin(a)[2:] #110010

#二进制转换为十进制
a='1010'
#int(x, base) string->number
print int(a,2) #10
a='1a'
print int(a,16) #26