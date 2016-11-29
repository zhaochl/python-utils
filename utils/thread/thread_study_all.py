#!/usr/bin/env python
# coding=utf-8
"""
熟练掌握Thread、Lock、Condition就可以应对绝大多数需要使用线程的场合，
某些情况下local也是非常有用的东西。本文的最后使用这几个类展示线程基础中提到的场景
"""
import threading
 
alist = None
condition = threading.Condition()
 
def doSet():
    if condition.acquire():
        while alist is None:
            condition.wait()
        for i in range(len(alist))[::-1]:
            alist[i] = 1
        condition.release()
 
def doPrint():
    if condition.acquire():
        while alist is None:
            condition.wait()
        for i in alist:
            print i,
        print
        condition.release()
 
def doCreate():
    global alist
    if condition.acquire():
        if alist is None:
            alist = [0 for i in range(10)]
            condition.notifyAll()
        condition.release()
 
tset = threading.Thread(target=doSet,name='tset')
tprint = threading.Thread(target=doPrint,name='tprint')
tcreate = threading.Thread(target=doCreate,name='tcreate')
tset.start()
tprint.start()
tcreate.start()
