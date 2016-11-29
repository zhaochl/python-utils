#!/usr/bin/env python
# coding=utf-8
"""
Lock（指令锁）是可用的最低级的同步指令。Lock处于锁定状态时，不被特定的线程拥有。Lock包含两种状态——锁定和非锁定，以及两个基本的方法。
可以认为Lock有一个锁定池，当线程请求锁定时，将线程至于池中，直到获得锁定后出池。池中的线程处于状态图中的同步阻塞状态。
构造方法： 
Lock()
实例方法： 
acquire([timeout]): 使线程进入同步阻塞状态，尝试获得锁定。 
release(): 释放锁。使用前线程必须已获得锁定，否则将抛出异常
"""
import threading
import time
 
data = 0
lock = threading.Lock()
 
def func():
    global data
    print '%s acquire lock...' % threading.currentThread().getName()
    
    # 调用acquire([timeout])时，线程将一直阻塞，
    # 直到获得锁定或者直到timeout秒后（timeout参数可选）。
    # 返回是否获得锁。
    if lock.acquire():
        print '%s get the lock.' % threading.currentThread().getName()
        data += 1
        time.sleep(2)
        print '%s release lock...' % threading.currentThread().getName()
        
        # 调用release()将释放锁。
        lock.release()
def test():
    t1 = threading.Thread(target=func)
    t2 = threading.Thread(target=func)
    t3 = threading.Thread(target=func)
    t1.start()
    t2.start()
    t3.start()
if __name__=='__main__':
    test()
