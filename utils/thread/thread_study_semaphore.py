#!/usr/bin/env python
# coding=utf-8
"""
Semaphore（信号量）是计算机科学史上最古老的同步指令之一。Semaphore管理一个内置的计数器，每当调用acquire()时-1，调用release() 时+1。计数器不能小于0；当计数器为0时，acquire()将阻塞线程至同步锁定状态，直到其他线程调用release()。

基于这个特点，Semaphore经常用来同步一些有“访客上限”的对象，比如连接池。

BoundedSemaphore 与Semaphore的唯一区别在于前者将在调用release()时检查计数器的值是否超过了计数器的初始值，如果超过了将抛出一个异常。

构造方法： 
Semaphore(value=1): value是计数器的初始值。

实例方法： 
acquire([timeout]): 请求Semaphore。如果计数器为0，将阻塞线程至同步阻塞状态；否则将计数器-1并立即返回。 
release(): 释放Semaphore，将计数器+1，如果使用BoundedSemaphore，还将进行释放次数检查。release()方法不检查线程是否已获得 Semaphore
"""

import threading
import time
 
# 计数器初值为2
semaphore = threading.Semaphore(2)
 
def func():
    
    # 请求Semaphore，成功后计数器-1；计数器为0时阻塞
    print '%s acquire semaphore...' % threading.currentThread().getName()
    if semaphore.acquire():
        
        print '%s get semaphore' % threading.currentThread().getName()
        time.sleep(4)
        
        # 释放Semaphore，计数器+1
        print '%s release semaphore' % threading.currentThread().getName()
        semaphore.release()
 
t1 = threading.Thread(target=func)
t2 = threading.Thread(target=func)
t3 = threading.Thread(target=func)
t4 = threading.Thread(target=func)
t1.start()
t2.start()
t3.start()
t4.start()
 
time.sleep(2)
 
# 没有获得semaphore的主线程也可以调用release
# 若使用BoundedSemaphore，t4释放semaphore时将抛出异常
print 'MainThread release semaphore without acquire'
semaphore.release()
