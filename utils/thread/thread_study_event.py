#!/usr/bin/env python
# coding=utf-8
"""
Event（事件）是最简单的线程通信机制之一：一个线程通知事件，其他线程等待事件。Event内置了一个初始为False的标志，当调用set()时设为True，调用clear()时重置为 False。wait()将阻塞线程至等待阻塞状态。

Event其实就是一个简化版的 Condition。Event没有锁，无法使线程进入同步阻塞状态。

构造方法： 
Event()

实例方法： 
isSet(): 当内置标志为True时返回True。 
set(): 将标志设为True，并通知所有处于等待阻塞状态的线程恢复运行状态。 
clear(): 将标志设为False。 
wait([timeout]): 如果标志为True将立即返回，否则阻塞线程至等待阻塞状态，等待其他线程调用set()
"""

# encoding: UTF-8
import threading
import time
 
event = threading.Event()
 
def func():
    # 等待事件，进入等待阻塞状态
    print '%s wait for event...' % threading.currentThread().getName()
    event.wait()
    
    # 收到事件后进入运行状态
    print '%s recv event.' % threading.currentThread().getName()
 
t1 = threading.Thread(target=func)
t2 = threading.Thread(target=func)
t1.start()
t2.start()
 
time.sleep(2)
 
# 发送事件通知
print 'MainThread set event.'
event.set()
