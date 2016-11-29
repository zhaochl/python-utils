#!/usr/bin/env python
# coding=utf-8
def process(a,b,add=0,sub=0,mut=0,div=0):
    if add==1:
        return a+b
    if sub==1:
        return a-b
    if mut ==1:
        return a*b
    if div ==1:
        return a/b
print process(1,2,add=1)
print process(1,2,sub=1)
print process(1,2,mut=1)

