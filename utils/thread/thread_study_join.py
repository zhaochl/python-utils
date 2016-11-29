#!/usr/bin/env python
# coding=utf-8
# - author zcl
"""
实例方法： 
isAlive(): 返回线程是否在运行。正在运行指启动后、终止前。 
get/setName(name): 获取/设置线程名。 
is/setDaemon(bool): 获取/设置是否守护线程。初始值从创建该线程的线程继承。当没有非守护线程仍在运行时，程序将终止。 
start(): 启动线程。 
join([timeout]): 阻塞当前上下文环境的线程，直到调用此方法的线程终止或到达指定的timeout（可选参数）。

一个使用join()的例子：
in threadContext.
in threadJoin.
out threadJoin.
"""
import threading
import time
 
def context(tJoin):
    print 'in threadContext.'
    tJoin.start()
    
    # 将阻塞tContext直到threadJoin终止。
    tJoin.join()
    
    # tJoin终止后继续执行。
    print 'out threadContext.'
 
def join():
    print 'in threadJoin.'
    time.sleep(1)
    print 'out threadJoin.'
 
tJoin = threading.Thread(target=join)
tContext = threading.Thread(target=context, args=(tJoin,))
 
tContext.start()
