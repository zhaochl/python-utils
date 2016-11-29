#!/usr/bin/env python
# coding=utf-8
"""
Timer（定时器）是Thread的派生类，用于在指定时间后调用一个方法。

构造方法： 
Timer(interval, function, args=[], kwargs={}) 
interval: 指定的时间 
function: 要执行的方法 
args/kwargs: 方法的参数

实例方法： 
Timer从Thread派生，没有增加实例方法
"""
# encoding: UTF-8
import threading
 
def func():
    print 'hello timer!'
print 'waiting..5s'
timer = threading.Timer(5, func)
timer.start()
print 'over'
