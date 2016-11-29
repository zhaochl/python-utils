#!/usr/bin/env python
# coding=utf-8
import threading
"""
构造方法： 
Thread(group=None, target=None, name=None, args=(), kwargs={}) 
group: 线程组，目前还没有实现，库引用中提示必须是None； 
target: 要执行的方法； 
name: 线程名； 
args/kwargs: 要传入方法的参数。

实例方法： 
isAlive(): 返回线程是否在运行。正在运行指启动后、终止前。 
get/setName(name): 获取/设置线程名。 
is/setDaemon(bool): 获取/设置是否守护线程。初始值从创建该线程的线程继承。当没有非守护线程仍在运行时，程序将终止。 
start(): 启动线程。 
join([timeout]): 阻塞当前上下文环境的线程，直到调用此方法的线程终止或到达指定的timeout（可选参数）
""" 
# 方法1：将要执行的方法作为参数传给Thread的构造方法
def func():
    print 'func() passed to Thread'
    i=0
    while i<10:
        print 'func is running.'
        i+=1
 
t = threading.Thread(target=func)
print t.isAlive()
t.start()
print t.isAlive()
# 方法2：从Thread继承，并重写run()
class MyThread(threading.Thread):
    def run(self):
        print 'MyThread extended from Thread'
 
t = MyThread()
t.start()

