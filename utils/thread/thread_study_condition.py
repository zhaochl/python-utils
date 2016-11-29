#!/usr/bin/env python
# coding=utf-8
# authoer zcl
import threading
import time
from random import *
"""
Condition（条件变量）通常与一个锁关联。需要在多个Contidion中共享一个锁时，可以传递一个Lock/RLock实例给构造方法，否则它将自己生成一个RLock实例。
可以认为，除了Lock带有的锁定池外，Condition还包含一个等待池，池中的线程处于状态图中的等待阻塞状态，直到另一个线程调用notify()/notifyAll()通知；得到通知后线程进入锁定池等待锁定。

构造方法： 
Condition([lock/rlock])

实例方法： 
acquire([timeout])/release(): 调用关联的锁的相应方法。 
wait([timeout]): 调用这个方法将使线程进入Condition的等待池等待通知，并释放锁。使用前线程必须已获得锁定，否则将抛出异常。 
notify(): 调用这个方法将从等待池挑选一个线程并通知，收到通知的线程将自动调用acquire()尝试获得锁定（进入锁定池）；其他线程仍然在等待池中。调用这个方法不会释放锁定。使用前线程必须已获得锁定，否则将抛出异常。 
notifyAll(): 调用这个方法将通知等待池中所有的线程，这些线程都将进入锁定池尝试获得锁定。调用这个方法不会释放锁定。使用前线程必须已获得锁定，否则将抛出异常。

例子是很常见的生产者/消费者模式
"""
 
# 商品
product = None
# 条件变量
con = threading.Condition()
 
# 生产者方法
def produce():
    global product
    
    if con.acquire():
        while True:
            if product is None:
                data = randint(01,20)
                product = 'data is '+str(data)
                print 'produce...'+product
                
                # 通知消费者，商品已经生产
                con.notify()
            
            # 等待通知
            con.wait()
            time.sleep(2)
 
# 消费者方法
def consume():
    global product
    
    if con.acquire():
        while True:
            if product is not None:
                print 'consume...'+product
                product = None
                
                # 通知生产者，商品已经没了
                con.notify()
            
            # 等待通知
            con.wait()
            time.sleep(2)
if __name__=='__main__':
    t1 = threading.Thread(target=produce)
    t2 = threading.Thread(target=consume)
    """
    daemon 使该线程听从main 的退出
    """

    t1.setDaemon(True)
    t2.setDaemon(True)
    t2.start()
    t1.start()
    i=0
    while i<5:
        print 'main runing,i:'+str(i)
        i+=1
        time.sleep(1)
